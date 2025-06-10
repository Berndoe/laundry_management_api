from django.core.mail import EmailMultiAlternatives
from django.db import models, transaction
from rest_framework import status
from rest_framework.response import Response

from laundry_api.settings import EMAIL_HOST_USER
from common.viewsets import CustomViewSet
from orders.models import Orders, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer
from payments.models import Payment
from utils.pdf_generator import generate_pdf


class OrderViewSet(CustomViewSet):
    serializer_class = OrderSerializer
    search_fields = '__all__'
    ordering_fields = '__all__'
    filterset_fields = '__all__'

    def get_queryset(self):
        return Orders.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        """
        Save the order and its associated order items.
        """
        data = self.request.data
        company = self.request.user.company
        order_items = data.pop('order_items', [])  # Extract order items from the request data

        # Save the order
        order = serializer.save(company=company)

        # Create OrderItem entries
        order_item_objects = [
            OrderItem(
                order=order,
                item_id=item_data['item'],
                quantity=item_data['quantity'],  # Default quantity to 1
                company=company
            )
            for item_data in order_items
        ]
        OrderItem.objects.bulk_create(order_item_objects)  # Bulk creation for efficiency

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create an order, associated items, and calculate total price.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        order = serializer.instance
        order_items = OrderItem.objects.filter(order=order)

        # Calculate total price
        total_price = OrderItem.objects.filter(order=order).aggregate(
            total=models.Sum(
                models.F('item__price') * models.F('quantity')
            )
        )['total'] or 0

        payment = Payment(
            amount=total_price,
            customer_id=order.customer_id,
            order_id=order.id,
            company=self.request.user.company,
            payment_type='Cash',
            payment_date='2024-12-02'
        )

        payment.save()

        self.send_invoice(order_items, order, order.customer.email, total_price)

        return Response(
            {
                "order": serializer.data,
                "total_price": total_price
            },
            status=status.HTTP_201_CREATED,
        )

    def send_invoice(self, order_items, order, recipient_email, total_price):
        """
        Sends the customer an invoice.
        """
        pdf_file = generate_pdf(
            'customer_receipts.html',
            {'order_items': order_items, 'order': order, 'total_price': total_price})
        email = EmailMultiAlternatives(
            subject=f'Invoice for Order {order.id}',
            body=f'Dear {order.customer.full_name}, \n\nPlease find attached the receipt for your order.\n\nThank you!',
            from_email=EMAIL_HOST_USER,
            to=[recipient_email]
        )

        email.attach(f'Invoice_{order.id}.pdf', pdf_file.getvalue(), 'application/pdf')
        email.send()


class OrderItemViewSet(CustomViewSet):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return OrderItem.objects.filter(company=self.request.user.company)
