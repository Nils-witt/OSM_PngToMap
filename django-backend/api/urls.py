from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', views.health_check, name='health_check'),
    path('public-health/', views.public_health, name='public_health'),
    path('send-message/', views.send_websocket_message, name='send_websocket_message'),
]