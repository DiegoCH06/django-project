from django.urls import path
from .views import UserView
from .views import manage_user


urlpatterns = [
    path('', UserView.as_view()),
    path('<int:id>/', manage_user, name='manage_user')
]
