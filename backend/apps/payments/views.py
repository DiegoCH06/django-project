from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Payment, PaymentSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from apps.orders.models import Order, OrderSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class PaymentView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user.id)

        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(payments, request)

        orders_serializer = PaymentSerializer(result_page, many=True)

        return Response({
            "ok": True,
            "result": paginator.get_paginated_response(orders_serializer.data).data
        }, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        user = User()
        user.id = request.user.id

        orders_ids = request.data.get('orders', [])
        ids = [v['id'] for v in orders_ids]
        data['orders'] = ids
        payment_serializer = PaymentSerializer(data=data)
        if payment_serializer.is_valid():

            try:
                orders = Order.objects.filter(id__in=ids, user=user.id)
                if len(orders) != len(orders_ids):
                    return Response({
                        "ok": False,
                        "result": "some orders does not exist"
                    }, status=400)
            except Order.DoesNotExist:
                return Response({
                    "ok": False,
                    "result": "some orders does not exist"
                }, status=400)

            payment = Payment.objects.create(user=user, total=data['total'])
            i = 0
            for v in orders_ids:
                orders[i].paid += v['pay']
                orders[i].save()
                i+=1
            payment.orders.set(orders)
            return Response({
                "ok": True,
                "result": payment_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'ok': False,
            'result': payment_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'PUT', 'GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def manage_payment(request, id):
    try:
        payment = Payment.objects.get(id=id)
    except Payment.DoesNotExist:
        return Response({
            "ok": False,
            "result": f"Payment does not exist (id = {id})"
        }, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        payment.delete()
        return Response({
            "ok": True,
            "result": "Payment deleted"
        }, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        payment_serializer = PaymentSerializer(payment, data=request.data)
        if payment_serializer.is_valid():
            payment_serializer.save()
            return Response({
                "ok": True,
                "result": payment_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'ok': False,
            'result': payment_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        payment_serializer = PaymentSerializer(payment)
        data_response = payment_serializer.data
        data_response['orders'] = OrderSerializer(payment.order_set.all(), many=True).data
        return Response({
            "ok": True,
            'result': data_response
        }, status=status.HTTP_200_OK)
