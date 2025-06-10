from common.serializers import BaseSerializer
from rest_framework import serializers
from orders.models import Orders, OrderItem


class OrderItemSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = OrderItem
        fields = ['id', 'order', 'item', 'quantity', 'company']


class OrderSerializer(BaseSerializer):
    status = serializers.CharField(source="get_status_display", required=False)
    order_items = OrderItemSerializer(many=True, read_only=True) # linking order items automatically to order
    total_price = serializers.FloatField(read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Orders
        fields = ['id', 'customer', 'order_date',
                  'order_items', 'status', 'company', 'total_price']
