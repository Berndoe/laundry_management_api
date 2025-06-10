import uuid

from django.db import models

from accounts.models import Company, Customer
from catalogue.models import Item
from common.models import BaseModel


class Orders(BaseModel):
    """
    Creating orders from customers
    """
    PENDING = "PD"
    IN_PROGRESS = "IP"
    COMPLETED = "CT"

    ORDER_STATUS_CHOICES = [
        (PENDING, "Pending"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default=PENDING)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return (f'Order for Customer ID: {self.customer} '
                f'Order date: {self.order_date}'
                f'Status: {self.status}')


class OrderItem(BaseModel):
    """
    Details of the orders from customers
    """
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return (f'Order ID: {self.order}'
                f'Item: {self.item.name}'
                f'Quantity: {self.quantity}')

    @property
    def total_price(self):
        return self.item.price * self.quantity
