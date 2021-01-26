from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(UserAddress)
admin.site.register(Order)
