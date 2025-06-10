from rest_framework.routers import DefaultRouter

from catalogue import views

router = DefaultRouter()
router.register('items', views.ItemViewSet, basename='item')
router.register('services', views.ServiceViewSet, basename='service')
urlpatterns = router.urls
