from rest_framework import viewsets, filters
import django_filters.rest_framework


class CustomViewSet(viewsets.ModelViewSet):
    """This model is defined for viewsets of all models"""
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter,
                       django_filters.rest_framework.DjangoFilterBackend]
