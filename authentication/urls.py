from django.urls import path
from .views import Login


app_name = 'authentication'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
]