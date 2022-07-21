from django.contrib import admin
from .models import Shoes, Categories, Customer, Order, Cart, CartItem, OrderItem

# Register your models here.
admin.site.register(Shoes)
admin.site.register(Categories)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
