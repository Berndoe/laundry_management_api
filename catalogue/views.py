from catalogue.models import Item, Service
from catalogue.serializers import ItemSerializer, ServiceSerializer
from common.viewsets import CustomViewSet


class ItemViewSet(CustomViewSet):
    serializer_class = ItemSerializer
    search_fields = ['name', 'price', 'service']
    ordering_fields = ['name', 'price', 'service']
    filterset_fields = search_fields

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

    def get_queryset(self):
        return Item.objects.filter(company=self.request.user.company)


class ServiceViewSet(CustomViewSet):
    serializer_class = ServiceSerializer
    search_fields = '__all__'
    ordering_fields = search_fields
    filterset_fields = search_fields

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)

    def get_queryset(self):
        return Service.objects.filter(company=self.request.user.company)



