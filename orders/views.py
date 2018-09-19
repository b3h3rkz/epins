import random
from django.core.mail import EmailMessage
from string import ascii_uppercase, digits
import json
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
import requests
from requests.auth import HTTPBasicAuth
from .process_order import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from barbary.users.serializers import UserModelSerializer
from .serializers import (
    BuyOrderModelSerializer,
    AdminBuyOrderModelSerializer,
    SellOrderModelSerializer,
    AdminSellOrderModelSerializer,
    OrderAnalyticsModelSerializer,
    )
from .models import BuyOrder, BuyOrderDetail, SellOrder
from .permissions import IsOwner
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from rest_framework.decorators import list_route, detail_route
from wallet.models import Wallet
from currency.models import Currency


class BuyOrdersModelViewSet(ModelViewSet):
    model = BuyOrder
    serializer_class = BuyOrderModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BuyOrder.objects.filter(user=self.request.user).order_by('-modified_on')

    def create(self, request, *args, **kwargs):
        # generate a random unique value as order reference
        request.data['reference_id'] = settings.BUY_ORDER_PREFIX \
                                       + ''.join(random.sample((ascii_uppercase+digits), 4))\
                                       + 'L'

        validated_address = validate_address(request.data['address'], 'BTC')
        user_account_balance = self.get_account_balance(request.user.id)
        total_cost = self.calculate_total_cost(request.data['coin'], request.data['amount'])
        self.debit_wallet(total_cost, request.user.id)

        if total_cost > user_account_balance:
            return Response({"error": "Insufficient Funds"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not validated_address:
            return Response({"error": "Address is invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.data['amount'] < 10:
            return Response({"error": "Amount is less than minimum allowed"},
                            status=status.HTTP_400_BAD_REQUEST)

        else:
            send_btc = send(request.data['address'], request.data['amount'])
            if 'message' in send_btc:
                if send_btc['message'] == "Payment Sent":
                    request.data['fee'] = send_btc['fee']
                    request.data['cost'] = total_cost
                    request.data['transaction_id'] = send_btc['txid']
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    # Debit Wallet
                    self.debit_wallet(total_cost, request.user.id)
                    return Response(
                        {"success": "Successfully Funded Wallet"},
                        status=status.HTTP_201_CREATED,
                    )
            else:
                return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def get_account_balance(self, user_id):
        """
        get the user's wallet
        :param user_id:
        :return: string
        """
        wallet = Wallet.objects.get(user=user_id)
        return wallet.current_balance

    def debit_wallet(self, amount, user_id):
        """
        deduct amount from wallet
        :param amount:
        :param user_id:
        :return: float
        """
        wallet = Wallet.objects.get(user=user_id)
        wallet.current_balance = wallet.current_balance - amount
        wallet.save()
        return wallet.current_balance

    def calculate_total_cost(self, coin, amount):
        """
        get the price of the coin per USD in local currency
        :return: float
        """
        coin = Currency.objects.get(id=coin)
        total = amount * coin.buy_rate
        return total

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        subject = "Payment Confirmation on Bitnob"
        to = [request.user.email]
        # from_email = 'noreply@bitnob.com'

        ctx = {
            'user': request.user.username,
            'order': instance
        }

        message = get_template('emails/order_payment.html').render(Context(ctx))
        msg = EmailMessage()
        msg.subject = subject
        msg.body = message
        msg.to = to
        # msg.from_email = from_email
        msg.content_subtype = 'html'
        msg.send()

        return Response(serializer.data)

    @detail_route(methods=['post', 'put'])
    def receive_mobile_money(self, request, pk=None):
        payload = {
            'CustomerName': request.user.username,
            'CustomerMsisdn': '233' + request.data['transaction_phone'],
            'CustomerEmail': request.user.email,
            'Channel': request.data['network_name'],
            'Amount': 0.05,
            'PrimaryCallbackUrl': "https://62363896.ngrok.io/api/v1/buy_orders/mobile_money_callback/",
            'SecondaryCallbackUrl': "https://62363896.ngrok.io/api/v1/buy_orders/mobile_money_callback/",
            'Description': "DEPOSIT",
            'ClientReference': request.data['order'],
            "Token": ""
        }
        pay = requests.post(settings.HUBTEL_BASE_URL, data=payload, auth=('eaqhfpto', 'medxbcgv'))
        return HttpResponse(pay.content)

    @detail_route(methods=['get'])
    def get_momo_paid_order(self, request, pk=None):
        # this endpoint is polled to check if payment for an order has been made
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if len(instance.transaction_id) > 0:
            return Response({"success": "Payment Successful"}, data=serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"error": "Order Payment Was not completed", "paid": False},
            status=status.HTTP_404_NOT_FOUND)

    @csrf_exempt
    @list_route(methods=['post'])
    def mobile_money_callback(self, request):
        request_body_unicode = request.body.decode('utf-8')
        body = json.loads(request_body_unicode)
        order_id = body['Data']['ClientReference']
        print(order_id + 'order_id')
        instance = BuyOrder.objects.get(pk=order_id)
        print(instance + "instance")
        if body['ResponseCode'] == '0000':
            serializer = self.get_serializer(instance, data=instance, partial=True)
            instance.status = "processing"
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=200)
        else:
            return Response(status=400)


class AdminBuyOrdersModelViewset(ModelViewSet):
    model = BuyOrder
    serializer_class = AdminBuyOrderModelSerializer
    queryset = BuyOrder.objects.all().order_by('-modified_on')
    lookup_field = 'pk'
    permission_classes = [IsAdminUser]

    # def update(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     print(request.data)
    #     request.data['status'] = "processing"
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)


class SellOrderModelViewset(ModelViewSet):
    model = SellOrder
    serializer_class = SellOrderModelSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return SellOrder.objects.filter(user=self.request.user).order_by('-modified_on')

    def create(self, request, *args, **kwargs):
        request.data['reference_id'] = settings.SELL_ORDER_PREFIX \
                                       + ''.join(random.sample((ascii_uppercase+digits), 4))\
                                       + str(request.user.pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        subject = "Bitnob BTC Sale Order"
        to = [request.user.email]
        from_email = 'noreply@bitnob.com'
        ctx = {
            'user': request.user.username,
            'order': serializer.data
        }
        message = get_template('emails/sell_order.html').render(Context(ctx))
        msg = EmailMessage()
        msg.subject = subject
        msg.body = message
        msg.to = to
        msg.from_email = from_email
        msg.content_subtype = 'html'
        msg.send()
        return Response(
            {"success": "Order Created Successfully", "order": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers)


class AdminSellOrdersModelViewSet(ModelViewSet):
    model = SellOrder
    serializer_class = AdminSellOrderModelSerializer
    queryset = SellOrder.objects.all().order_by('-modified_on')
    permission_classes = _classes = [IsAdminUser]


class AdminOrderAnalyticsModelViewSet(ReadOnlyModelViewSet):
    model = BuyOrder
    serializer_class = OrderAnalyticsModelSerializer
    permission_classes = [IsAdminUser]
    queryset = BuyOrder.objects.all()[:1]









