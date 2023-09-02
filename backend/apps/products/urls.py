from django.urls import path
from .views import ProductView
from .views import manage_product


urlpatterns = [
    path('', ProductView.as_view()),
    path('<int:id>/', manage_product, name='manage_product')
]
