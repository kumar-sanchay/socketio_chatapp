from django.urls import path
from .views import index


app_name = 'socketio_app'

urlpatterns = [
    path('socket/', index, name='index'),
]