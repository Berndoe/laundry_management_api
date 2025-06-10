from rest_framework import serializers
from catalogue.models import Item, Service
from common.serializers import BaseSerializer


class ServiceSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Service
        fields = ['id', 'name', 'company']


class ItemSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Item
        fields = ['id', 'service', 'price', 'name', 'company']
