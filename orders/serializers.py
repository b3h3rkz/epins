from django.template import Context
from django.template.loader import get_template
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
    CurrentUserDefault,
    ReadOnlyField,
    RelatedField,
    HiddenField, PrimaryKeyRelatedField,
    HyperlinkedIdentityField
)

from rest_framework import serializers
from .models import BuyOrder, BuyOrderDetail, SellOrder, ORDER_STATUS
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage


class OrderAnalyticsModelSerializer(ModelSerializer):
    class Meta:
        model = BuyOrder
        lookup_field = "pk"
        fields = ('total_orders',
                  'total_sales',
                  'orders_processing',
                  'pending_orders',
                  'completed_orders',)


class BuyOrderModelSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    coin_name = serializers.ReadOnlyField(source='currency.name')

    class Meta:
        model = BuyOrder
        lookup_field = 'pk'
        fields = (
                  'id',
                  'user',
                  'address',
                  'amount',
                  'cost',
                  'fee',
                  'coin',
                  'coin_name',
                  'reference_id',
                  'transaction_id',
                  'created',
                  )
        read_only_fields = ('id',)


class AdminBuyOrderModelSerializer(BuyOrderModelSerializer):
    pass


class SellOrderModelSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(
        read_only=True,
        default=CurrentUserDefault())

    currency_name = serializers.ReadOnlyField(source='currency.name')

    class Meta:
        model = SellOrder
        lookup_field = 'pk'
        fields = (
                  'id',
                  'amount',
                  'amount_to_receive',
                  'currency',
                  'currency_name',
                  'reference_id',
                  'tx_hash',
                  'network_name',
                  'phone_number',
                  'bank_name',
                  'bank_account_number',
                  'bank_branch',
                  'note',
                  'account_name',
                  'created',
                  'user',
                  'status',
                  )
        read_only_fields = ('id',)


class AdminSellOrderModelSerializer(SellOrderModelSerializer):

    def update(self, instance, validated_data):
        if instance.status == 'pending':
            instance.status = 'processing'

        if instance.status == 'processing':
            instance.status = 'completed'
            subject = "Bitnob Order Completed"
            to = [instance.user.email]
            from_email = 'noreply@bitnob.com'
            ctx = {
                'user': instance.user.username,
                'order': instance
            }
            message = get_template('emails/sell_order_completed.html').render(Context(ctx))
            msg = EmailMessage()
            msg.subject = subject
            msg.body = message
            msg.to = to
            msg.from_email = from_email
            msg.content_subtype = 'html'
            msg.send()

        instance.save()
        return instance




