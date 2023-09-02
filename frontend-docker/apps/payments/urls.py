from django.urls import path
from .views import (
    list_payments,
    create_payment,
    delete_payment,
    select_order
)

urlpatterns = [
    path('', list_payments, name='list_payments'),
    path('create/', create_payment, name='CreatePayment'),
    path('delete/<int:payment_id>', delete_payment, name='DeletePayment'),
    path('select_order/', select_order, name='SelectOrder'),
]