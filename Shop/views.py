from Shop.models import Good, GoodInCart
from account.models import Customer
from rest_framework.decorators import api_view
from Shop.serializers import GoodSerializer, GoodInCartSerializer
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def goods(request):
    if request.method == 'GET':
        goods = Good.objects.all()
        serializer = GoodSerializer(goods, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = GoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def good_edit(request, id):
    try:
        good = Good.objects.get(pk=id)
    except Good.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        serializer = GoodSerializer(good)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = GoodSerializer(good, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        good.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def cart_list(request):
    objects = GoodInCart.objects.all()
    serializer = GoodInCartSerializer(objects, many=True)
    return Response(data=serializer.data)

@api_view(['POST', 'DELETE'])
def cart(request):
    if request.method == 'POST':
        serializer = GoodInCartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data={'message': 'Data is not valid'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            cart_item = GoodInCart.objects.get(good=request.data['good'], customer=request.data['customer'])
        except GoodInCart.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        cart_item.delete()
        return Response(data={'message': 'Good is deleted from cart'}, status=status.HTTP_204_NO_CONTENT)

