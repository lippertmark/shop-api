from django.db import models


class Good(models.Model):
    name = models.CharField(max_length=256)
    price = models.IntegerField()

    def __str__(self):
        return self.name + ' ' + str(self.price)


class GoodInCart(models.Model):
    customer = models.ForeignKey('account.Customer', on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.__str__() + ' - ' + self.good.__str__()

    def cart_items(self, customer_id):
        items = self.objects.filter(customer=customer_id)
        return items


class Order(models.Model):
    customer = models.ForeignKey('account.Customer', on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0) # full price
    coins_discount = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return str(self.pk) + ' - ' + self.customer.__str__()


class GoodInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)

    def __str__(self):
        return self.order.__str__() + ': ' + self.good.__str__()
