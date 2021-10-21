from django.contrib import admin
from .models import Orders,Address

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'default'
    ]

admin.site.register(Orders)
admin.site.register(Address)
