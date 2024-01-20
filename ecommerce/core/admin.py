from django.contrib import admin
from core.models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Catagory)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(CheckoutAddress)