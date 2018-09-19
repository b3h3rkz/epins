import json
from django.db import models
from django.conf import settings
from currency.models import Currency

ORDER_STATUS = (
    ('pending', 'PENDING'),
    ('processing', 'PROCESSING'),
    ('completed', 'COMPLETED'),
    ('cancelled', 'CANCELLED'),
    ('flagged', 'FLAGGED'),
)


class BuyOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coin = models.ForeignKey(Currency,  on_delete=models.CASCADE,  related_name="currency")
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.CharField(max_length=256)
    transaction_id = models.CharField(max_length=256)
    reference_id = models.CharField(max_length=256, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_id

    def total_orders(self):
        total = 0
        buy_orders = BuyOrder.objects.count()
        sell_orders = SellOrder.objects.count()
        total = buy_orders + sell_orders
        return total

    def total_sales(self):
        total = 0
        completed_orders = BuyOrder.objects.filter(status='completed')
        for order in completed_orders:
            total += order.amount_paid
        return total

    def completed_orders(self):
        completed_orders = BuyOrder.objects.filter(status='completed').count()
        return completed_orders

    def pending_orders(self):
        pending_orders = BuyOrder.objects.filter(status='pending')
        return pending_orders.count()

    def orders_processing(self):
        processing_orders = BuyOrder.objects.filter(status='pending')
        return processing_orders.count()


class BuyOrderDetail(models.Model):
    order = models.ForeignKey(BuyOrder,  on_delete=models.CASCADE, related_name='order')
    transaction_id = models.CharField(max_length=20, default='')
    network_name = models.CharField(max_length=20, default='')
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class SellOrder(models.Model):

    ORDER_STATUS = (
        ('pending', 'PENDING'),
        ('processing', 'PROCESSING'),
        ('completed', 'COMPLETED'),
        ('cancelled', 'CANCELLED'),
        ('flagged', 'FLAGGED'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_to_receive = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    currency = models.ForeignKey(Currency,  on_delete=models.CASCADE, related_name="selling_currency")
    reference_id = models.CharField(max_length=256, unique=True)
    network_name = models.CharField(max_length=20, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    bank_account_number = models.IntegerField(null=True)
    bank_branch = models.CharField(max_length=50, null=True)
    bank_name = models.CharField(max_length=50, null=True)
    account_name = models.CharField(max_length=30)
    tx_hash = models.CharField(max_length=250, default='')
    note = models.CharField(max_length=250, null=True)
    status = models.CharField(choices=ORDER_STATUS, default='pending', max_length=12)
    created = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)





