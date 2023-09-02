from django.urls import path
from .views import PaymentView
from .views import manage_payment


urlpatterns = [
    path('', PaymentView.as_view()),
    path('<int:id>/', manage_payment, name='manage_payment')
]
