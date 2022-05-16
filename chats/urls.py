from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('active_chat/<str:pk>/', views.active_chat, name='active-chat'),
    path('send_message/', views.send_message, name='send-message'),
    path('chat_search/', views.chat_search, name='chat-search'),
]