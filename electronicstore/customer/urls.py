from django.urls import path
from .views import (RegistrationView,
                    SignInView,
                    HomePageView,
                    update_details,
                    ViewProduct,
                    add_to_cart,
                    MyCart,
                    DeleteFromCart,
                    place_order,
                    view_orders,cancel_order,
                    CheckoutView)
urlpatterns=[
    path('register',RegistrationView.as_view(),name='register'),
    path('login',SignInView.as_view(),name='cust_signin'),
    path('home',HomePageView.as_view(),name='customer_home'),
    path("update",update_details,name="update"),
    path('viewproduct/<int:pk>',ViewProduct.as_view(),name='viewproduct'),
    path('addtocart/<int:pk>',add_to_cart,name='addtocart'),
    path('mycart',MyCart.as_view(),name='mycart'),
    path('removeitem/<int:pk>',DeleteFromCart.as_view(),name='deletecart'),
    path("placeorder/<int:id>/<int:cid>",place_order,name="placeorder"),
    path("vieworders", view_orders, name="vieworders"),
    path("removeorder/<int:id>",cancel_order,name="removeorder"),
    path("checkout", CheckoutView.as_view(), name="checkout"),

]
