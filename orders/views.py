import random
from django.core.mail import EmailMessage
from string import ascii_uppercase, digits
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
import requests
from requests.auth import HTTPBasicAuth
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from barbary.users.serializers import UserModelSerializer
from .serializers import (
    BuyOrderModelSerializer,
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

        user_account_balance = self.get_account_balance(request.user.id)
        total_cost = self.calculate_total_cost(request.data['coin'], request.data['amount'])
        self.debit_wallet(total_cost, request.user.id)

        if total_cost > user_account_balance:
            return Response({"error": "Insufficient Funds"},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.data['amount'] < 10:
            return Response({"error": "Amount is less than minimum allowed"},
                            status=status.HTTP_400_BAD_REQUEST)

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










