from django.shortcuts import render
from account.models import Customer
from Shop.models import GoodInCart, Order, GoodInOrder
from account.serializers import CustomerSerializer
from Shop.serializers import OrderSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def customers(request):
    if request.method == 'GET':
        customers_list = Customer.objects.all()
        serializer = CustomerSerializer(customers_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def customer_edit(request, customer_id):
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def clean_cart(request, customer_id):
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        customer.clean_cart()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def buy(request, customer_id):
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        cart_items = customer.cart_items()
        amount = 0
        order = Order(customer=customer)
        order.save()
        for item in cart_items:
            amount += item.good.price
            good_in_order = GoodInOrder(order=order, good=item.good)
            good_in_order.save()
        coins = 0
        if 'coins' in request.data:
            coins = request.data['coins']
            if coins > customer.coins:
                return Response({'message': 'Not enough coins'}, status=status.HTTP_400_BAD_REQUEST)
            elif coins > amount:
                return Response({'message': 'More than order amount'}, status=status.HTTP_400_BAD_REQUEST)
        order.amount = amount
        order.coins_discount = coins
        order.total = order.amount - order.coins_discount
        customer.coins -= coins
        order.save()
        customer.sum_of_orders += amount
        customer.cashback_coins(amount=amount)
        customer.check_level()
        customer.save()
        customer.clean_cart()
        serializer = OrderSerializer(order)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
