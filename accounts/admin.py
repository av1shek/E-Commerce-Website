from django.contrib import admin
from .models import Customer, User


admin.site.register(User)
admin.site.register(Customer)


