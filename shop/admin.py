from django.contrib import admin

# Register your models here.
from .models import Product, Orders, Message, OrderStatus

admin.site.register(Product)
admin.site.register(Orders)
admin.site.register(OrderStatus)
admin.site.register(Message)