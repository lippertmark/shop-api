from django.contrib import admin
from Shop.models import Good, GoodInCart, Order, GoodInOrder


admin.site.register(Good)
admin.site.register(GoodInCart)
admin.site.register(Order)
admin.site.register(GoodInOrder)