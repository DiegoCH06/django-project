from django.urls import path
from .views import (
    form_product,
    list_products,
    add_product_to_car,
    subtract_product,
    clean_car, save_order,
    delete_product,
    create_product,
    update_product
)

urlpatterns = [
    path('', list_products, name='product_list'),
    path('nuevo/', form_product, name='product_create'),
    path('add-product/<int:product_id>', add_product_to_car, name='add-product'),
    path('subtract_product/<int:product_id>', subtract_product, name='SubtractProduct'),
    path('clean_car/', clean_car, name='CleanCar'),
    path('save_order', save_order, name='SaveOrder'),
    path('delete_product/<int:product_id>', delete_product, name='DeleteProduct'),
    path('create_product/', create_product, name='CreateProduct'),
    path('update_product/<int:product_id>', update_product, name='UpdateProduct'),
]
