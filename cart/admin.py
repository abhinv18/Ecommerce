from django.contrib import admin
from cart.models import Cart,Order,Order_item

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Order_item)

