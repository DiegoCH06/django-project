from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Shipment, ShipmentSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from apps.orders.models import Order, OrderSerializer


# Create your views here.
class ShipmentView(CreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    def get(self, request):
        shipments = Shipment.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(shipments, request)

        shipments_serializer = ShipmentSerializer(result_page, many=True)

        return Response({
            "ok": True,
            "result": paginator.get_paginated_response(shipments_serializer.data).data
        }, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data

        orders_ids = request.data.get('orders', [])
        shipment_serializer = ShipmentSerializer(data=data)
        if shipment_serializer.is_valid():

            try:
                orders = Order.objects.filter(id__in=orders_ids)
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

            shipment = Shipment.objects.create(type=request.data['type'])
            shipment.orders.set(orders)

            return Response({
                "ok": True,
                "result": ShipmentSerializer(shipment).data
            }, status=status.HTTP_200_OK)

        return Response({
            'ok': False,
            'result': shipment_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', 'PUT', 'GET'])
@csrf_exempt
def shipment_order(request, id):
    try:
        shipment = Shipment.objects.get(id=id)
    except Shipment.DoesNotExist:
        return Response({
            "ok": False,
            "result": f"Shipment does not exist (id = {id})"
        }, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        shipment.delete()
        return Response({
            "ok": True,
            "result": "Shipment deleted"
        }, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        shipment_serializer = ShipmentSerializer(shipment, data=request.data)
        if shipment_serializer.is_valid():
            shipment_serializer.save()
            return Response({
                "ok": True,
                "result": shipment_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'ok': False,
            'result': shipment_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        payment_serializer = ShipmentSerializer(shipment)
        data_response = payment_serializer.data
        # data_response['orders'] = OrderSerializer(payment.order_set.all(), many=True).data
        return Response({
            "ok": True,
            'result': data_response
        }, status=status.HTTP_200_OK)
