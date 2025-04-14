from django.contrib import admin
from carts.models import Cart, CartItem, CartSession

admin.site.register(Cart)
admin.site.register(CartSession)
admin.site.register(CartItem)