from common.viewsets import CustomViewSet
from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentViewSet(CustomViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(company=self.request.user.company)

