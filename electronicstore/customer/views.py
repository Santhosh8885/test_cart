from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from .forms import RegistrationForm, LoginForm,UpdateForm,PlaceOrderForm,AddressForm
from customer.models import Cart,Orders,Address
from seller.models import Products
from django.views.generic import ListView, DetailView, View
from django.contrib import messages


class RegistrationView(TemplateView):
    form_class = RegistrationForm
    template_name = "registration.html"
    model = User
    context = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context["form"] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cust_signin")


class SignInView(TemplateView):
    template_name = "login.html"
    form_class = LoginForm
    context = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        self.context["form"] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("customer_home")
            else:
                self.context["form"] = form
                return render(request, self.template_name, self.context)


class HomePageView(TemplateView):
    template_name = 'homepage.html'
    context={}
    def get(self, request, *args, **kwargs):
        products = Products.objects.all()
        self.context['products']=products
        return render(request, self.template_name,self.context)


def signout(request):
    logout(request)
    return redirect("signin")

def update_details(request):
    # detail=Userdetails.objects.get()
    form = UpdateForm()
    if request.method == "GET":
        context = {"form": form}
        return render(request, "user_details.html", context)
    elif request.method == "POST":
        form = UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("customer_home")
        else:
            context = {"form": form}
            return render(request, "user_details.html", context)


class ViewProduct(TemplateView):
    template_name = 'productdetail.html'
    context={}
    def get(self, request, *args, **kwargs):
        id=kwargs['pk']
        product=Products.objects.get(id=id)
        self.context['product']=product
        return render(request,self.template_name,self.context)

def add_to_cart(request,*args,**kwargs):
    id=kwargs['pk']
    product=Products.objects.get(id=id)
    cart=Cart(product=product,user=request.user)
    cart.save()
    return redirect('mycart')

class MyCart(TemplateView):
    template_name = 'cart.html'
    context={}
    def get(self, request, *args, **kwargs):
        cart_products=Cart.objects.filter(user=request.user,status='ordernotplaced')
        self.context['cart_products']=cart_products
        return render(request,self.template_name,self.context)

class DeleteFromCart(TemplateView):
    def get(self, request, *args, **kwargs):
        id=kwargs['pk']
        cart_product=Cart.objects.get(id=id)
        cart_product.delete()
        return redirect('mycart')

def place_order(request,*args,**kwargs):
    id=kwargs.get("id")
    product=Products.objects.get(id=id)
    instance={
        "product":product.product_name
    }
    form=PlaceOrderForm(initial=instance)
    context={}
    context["form"]=form

    if request.method=="POST":
        cid=kwargs.get("cid")
        cart=Cart.objects.get(id=cid)

        form=PlaceOrderForm(request.POST)
        if form.is_valid():
            # address=form.cleaned_data.get("address")
            product=product
            order=Orders(product=product,user=request.user,seller=product.user.username)
            print(product.user.username)
            order.save()
            cart.status="orderplaced"
            cart.save()
            return redirect("checkout")

    return render(request,"placeorder.html",context)

def view_orders(request,*args,**kwargs):
    orders=Orders.objects.filter(user=request.user,status="ordered")

    context={
        "orders":orders,
    }
    return render(request,"vieworders.html",context)

def cancel_order(request,*args,**kwargs):
    id=kwargs.get("id")
    order=Orders.objects.get(id=id)
    order.status="cancelled"
    order.save()
    return redirect("vieworders")

class CheckoutView(View):
    def get(self, *args, **kwargs):
        print(self.kwargs)
        id = kwargs.get("id")
        # product = Products.objects.get(id=id)
        form = AddressForm()
        order = Orders.objects.get(user=self.request.user, status="ordered")
        print(len(order))
        context = {
            'form': form,
            'order': order
        }
        return render(self.request, 'checkout.html',context)
    def post(self, *args, **kwargs):
        order = Orders.objects.filter(user=self.request.user, status="ordered")
        print(order)
        print(len(order))

        form = AddressForm(self.request.POST or None)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            save_info = form.cleaned_data.get('save_info')
            use_default = form.cleaned_data.get('use_default')
            payment_option = form.cleaned_data.get('payment_option')

            address = Address(
                user=self.request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                zip=zip,
            )
            address.save()
            if save_info:
                address.default=True
                address.save()
            order.address = address
            print(address)
            order.save()
            print(form.cleaned_data)
            return redirect('checkout')
        else:
            print('form invalid')
            return redirect('checkout')
