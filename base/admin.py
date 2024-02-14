from django.contrib import admin
from .models import Profile, Balance, Order, Shipping

admin.site.register(Profile)
admin.site.register(Balance)
admin.site.register(Order)
admin.site.register(Shipping)