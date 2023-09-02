from django.urls import path
from .views import ShipmentView
from .views import shipment_order


urlpatterns = [
    path('', ShipmentView.as_view()),
    path('<int:id>/', shipment_order, name='shipment_order')
]
