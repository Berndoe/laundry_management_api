from common.serializers import BaseSerializer
from payments.models import Payment


class PaymentSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Payment
        fields = ['id', 'amount', 'order',
                  'payment_type', 'payment_status', 'payment_date']
