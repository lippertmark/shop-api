from rest_framework import serializers
from Shop.models import Good, GoodInCart, Order, GoodInOrder
from account.serializers import CustomerSerializer


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = '__all__'


class GoodInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodInCart
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['customer'] = CustomerSerializer(read_only=True)
        self.fields['good'] = GoodSerializer(read_only=True)
        return super(GoodInCartSerializer, self).to_representation(instance)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['customer'] = CustomerSerializer(read_only=True)
        return super(OrderSerializer, self).to_representation(instance)


class GoodInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodInOrder
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['order'] = OrderSerializer(read_only=True)
        self.fields['good'] = GoodSerializer(read_only=True)
        return super(GoodInOrderSerializer, self).to_representation(instance)
