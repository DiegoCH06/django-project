from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Product, ProductSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ProductView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(products, request)

        products_serializer = ProductSerializer(result_page, many=True)

        return Response({
            "ok": True,
            "result": paginator.get_paginated_response(products_serializer.data).data
        }, status=status.HTTP_200_OK)


@api_view(['DELETE', 'PUT', 'GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def manage_product(request, id):
    print(request.data)
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({
            "ok": False,
            "result": f"Product does not exist (id = {id})"
        }, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        product.delete()
        return Response({
            "ok": True,
            "result": "Product deleted"
        }, status=status.HTTP_200_OK)
    elif request.method == 'PUT':

        product_serializer = ProductSerializer(product, data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({
                "ok": True,
                "result": product_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'ok': False,
            'result': product_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        product_serializer = ProductSerializer(product)
        return Response({
            "ok": True,
            'result': product_serializer.data
        }, status=status.HTTP_200_OK)
