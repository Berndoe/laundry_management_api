import datetime
import uuid
from django.db import models
from accounts.models import Company
from accounts.models import Customer
from orders.models import Orders
from common.models import BaseModel


class Payment(BaseModel):
    """
    The model for Payment details
    """

    # payment options
    CASH = "CS"
    BANK_CARD = "BC"
    MOMO = "MO"

    PAYMENT_OPTIONS = {
        CASH: "Cash",
        BANK_CARD: "Bank Card",
        MOMO: "Momo",
    }

    # payment status
    PAID = "PD"
    PENDING = "PN"

    PAYMENT_STATUS = {
        PAID: "Paid",
        PENDING: "Pending",
    }
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='payments')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=50, choices=PAYMENT_OPTIONS, default=CASH)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default=PENDING)
    payment_date = models.DateTimeField()

    class Meta:
        db_table = "payments"

    def __str__(self):
        return f'Payment: {Payment}'

