from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Order, OrderSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from apps.products.models import Product
from django.contrib.auth.models import User


# Create your views here.
class OrderView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user.id)

        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(orders, request)

        orders_serializer = OrderSerializer(result_page, many=True)

        return Response({
            "ok": True,
            "result": paginator.get_paginated_response(orders_serializer.data).data
        }, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        user = request.user

        # products_ids = request.data['products']

        order_serializer = OrderSerializer(data=data)
        if order_serializer.is_valid():
            products_ids = order_serializer['products']
            try:
                products = Product.objects.filter(id__in=products_ids.value)
                if len(products) != len(products_ids.value):
                    return Response({
                        "ok": False,
                        "result": "some products does not exist"
                    }, status=400)
            except Product.DoesNotExist:
                return Response({
                    "ok": False,
                    "result": "some products does not exist"
                }, status=400)
            print(user.id)
            user_r = User()
            user_r.id=user.id
            order = Order.objects.create(user=user_r, paid=data['paid'], total=data['total'])
            order.products.set(products)
            order_serializer = OrderSerializer(order)
            return Response({
                "ok": True,
                "result": order_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'ok': False,
            'result': order_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'PUT', 'GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def manage_order(request, id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return Response({
            "ok": False,
            "result": f"Order does not exist (id = {id})"
        }, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        order.delete()
        return Response({
            "ok": True,
            "result": "Order deleted"
        }, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        order_serializer = OrderSerializer(order, data=request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response({
                "ok": True,
                "result": order_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'ok': False,
            'result': order_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        order_serializer = OrderSerializer(order)
        print(order_serializer.data)
        return Response({
            "ok": True,
            'result': order_serializer.data
        }, status=status.HTTP_200_OK)
