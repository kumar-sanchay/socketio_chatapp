from django.urls import path
from .views import Dashboard, Chat, index


app_name = 'chat'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('chat/<int:pk>/<slug:username>', Chat.as_view(), name='chat_page'),
]