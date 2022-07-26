from django.db import models
from Shop.models import GoodInCart


class Customer(models.Model):
    username = models.CharField(max_length=300)
    sum_of_orders = models.IntegerField(default=0)
    coins = models.FloatField(default=0.0)
    level = models.IntegerField(default=1)

    def clean_cart(self):
        cart_items = GoodInCart.objects.filter(customer=self.pk)
        for item in cart_items:
            item.delete()

    def cart_items(self):
        cart_items = GoodInCart.objects.filter(customer=self.pk)
        return cart_items

    def cashback_coins(self, amount):
        self.coins += (self.level / 100) * amount

    def check_level(self):
        if self.sum_of_orders > 5000:
            self.level = 5
        else:
            self.level = int(self.sum_of_orders // 1000) + 1

    def __str__(self):
        return self.username
