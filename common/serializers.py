from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    """
    The base serializer for all serializers
    """
    class Meta:
        extra_kwargs = {'company': {'required': True}}
