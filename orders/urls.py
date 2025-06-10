from django.urls import path
from rest_framework.routers import DefaultRouter
from orders import views

router = DefaultRouter()
router.register('order-items', views.OrderItemViewSet, basename='order-items')
router.register('orders', views.OrderViewSet, basename='orders')

urlpatterns = router.urls
