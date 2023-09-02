from django.urls import path
from .views import OrderView
from .views import manage_order


urlpatterns = [
    path('', OrderView.as_view()),
    path('<int:id>/', manage_order, name='manage_product')
]
