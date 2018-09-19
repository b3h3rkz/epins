import random
from string import ascii_uppercase, digits

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.core.exceptions import ObjectDoesNotExist

from wallet.serializers import (WalletModelSerializer, 
                                DepositModelSerializer,
                                WithdrawalModelSerializer,
                                BeneficiaryBankModelSerializer,
                                BeneficiaryMobileMoneyModelSerializer,
                                ManualDepositModelSerializer,
                                )

from wallet.models import (Wallet,
                           Deposit,
                           ManualDeposit,
                           Withdrawal,
                           BeneficiaryBank,
                           BeneficiaryMobileMoney,)

from rest_framework.decorators import list_route, detail_route
from .choices import *
import hashlib
import requests
from django.conf import settings
from voucher.models import Voucher





class ManualDepositModelViewSet(ModelViewSet):
    model = ManualDeposit
    serializer_class = ManualDepositModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """get all transactions from this user's wallet """
        return ManualDeposit.objects.filter(user=self.request.user.id).order_by('created_at')

    @detail_route(methods=['PUT'])
    def paid_request(self, request, pk=None):
        instance = self.get_object()
        instance.status = PROCESSING
        instance.save()
        return Response("Deposit Request Submitted")


class DepositModelViewSet(ModelViewSet):
    model = Deposit
    serializer_class = DepositModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Deposit.objects.filter(wallet__user=self.request.user.id)


class WithdrawalModelViewSet(ModelViewSet):
    model = Withdrawal
    serializer_class = WithdrawalModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Withdrawal.objects.filter(wallet__user=self.request.user.id)

    def create(self, request, *args, **kwargs):
        """
        mental note: find best way to query for wallet, should we take the wallet based on the user or from the request
        :param request:
        :param args:
        :param kwargs:
        :return: serialized object
        """
        wallet = Wallet.objects.filter(user=self.request.user.id)
        wallet = Wallet.objects.get(id=wallet)
        request.data['status'] = PENDING

        if request.data['value'] > wallet.current_balance:
            return Response("Insufficient Balance")
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            wallet.current_balance = wallet.current_balance - request.data['value']
            wallet.save()
            return Response(serializer.data)


class WalletModelViewSet(ModelViewSet):
    model = Wallet
    serializer_class = WalletModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user.id)

    @list_route(methods=['POST'])
    def get_payment_info(self, request):
        instance = Wallet.objects.get(id=request.data['wallet'])
        id = request.data['transaction_id']
        url = 'https://voguepay.com/?v_transaction_id=' + id + '&type=json&demo=true'
        response = requests.get(url).json()
        total = int(response['total_credited_to_merchant'])
        instance.current_balance += total
        instance.save()
        total = int(response['total_credited_to_merchant'])
        deposit = Deposit(wallet=instance,
                          value=total,
                          ref_code=id)
        deposit.save()
        return Response('Successfully Deposited Funds')

    @detail_route(methods=['PUT'])
    def vogue_pay_request(self, request, pk=None):
        url = "https://voguepay.com/"
        headers = {'Content-Type': 'application/json'}
        payload = {
         "total": request.data['amount'],
         "memo": "Funds Deposit by ",
         "name": request.user.first_name + ' ' + request.user.last_name,
         "email": request.user.email,
         "developer_code": "ddd",
         "cur": request.data['currency'],
         "v_merchant_id": "demo",
         "merchant_ref": "BTBDEP" + ''.join(random.sample((ascii_uppercase + digits), 4)),
         "p": "linkToken"
          }
        response = requests.get(url, params=payload, headers=headers)
        return Response({'payurl': response.text, 'payload': payload})


    @detail_route(methods=['PUT'])
    def ravepayment_request(self, request, pk=None, *args, **kwargs):
        hashedPayload = ''
        payload = {
            "PBFPubKey": 'FLWPUBK-3d15ffa5c7ec93883c651c0f441bc2d0-X',
            "amount": request.data['amount'],
            "payment_method": "both",
            "custom_description": "Bitnob Exchange",
            "custom_logo": "https://bitnob.com/img/1.png",
            "custom_title": "Deposit Funds to Bitnob",
            "country": request.data['country'],
            "currency": request.data['currency'],
            "customer_email": request.user.email,
            "customer_firstname": request.user.first_name,
            "customer_lastname": request.user.last_name,
            "customer_phone": request.data['phone'],
            "txref": "MG-" + ''.join(random.sample((ascii_uppercase+digits), 4))
        }
    # sort payload and concatenate into a single string
        sorted_payload = sorted(payload)

    # concatenate sorted_payload. The payload is rearranged and the values concatenated in the order of the sorted keys.
        hashed_payload = ''
        for value in sorted_payload:
            hashed_payload += value
        hashed_string = hashed_payload + "FLWSECK-b86e4802fc5eaa03db5e7f73fdc4514e-X"
        integrity_hash = hashlib.sha256(hashed_string.lower().encode()).hexdigest()
        return Response({'payload': payload, 'integrityHash': integrity_hash})

    @detail_route(methods=['PUT'])
    def ravepay_deposit(self, request, pk=None):
        instance = self.get_object()
        url = "https://ravesandboxapi.flutterwave.com/flwv3-pug/getpaidx/api/xrequery"

        data = {
            "txref": request.data['tx']['txRef'],  # this is the reference from the
                                                   # payment button response after customer paid.
            "SECKEY": "FLWSECK-b86e4802fc5eaa03db5e7f73fdc4514e-X",  # this is the secret key of
                                                                     # the pay button generated
            "include_payment_entity": 1

        }
        response = requests.post(url, data=data).json()

        # confirm that the response for the transaction is successful
        if response['status'] == 'success':
            # confirm that the amount for that transaction is the amount you wanted to charge
            if response['data']['chargecode'] == '00':
                if response['data']['amount'] == request.data['amount']:
                        instance.current_balance += response['data']['amount']
                        instance.save()
                        # log new deposit
                        deposit = Deposit(wallet=instance,
                                          value=response['data']['amount'],
                                          ref_code=request.data['tx']['txRef'])
                        deposit.save()
                        return Response('Successfully Deposited Funds')
                return Response({"error": "amount not equal to submitted funds"})
            return Response({"error": "transaction failed"})
        return Response({"errror": "No Transaction Found"})

    @detail_route(methods=['PUT'], serializer_class=DepositModelSerializer)
    def deposit(self, request, pk=None):
        instance = self.get_object()
        ref_code = ''.join(random.sample((ascii_uppercase+digits), 8))
        deposit = Deposit(wallet=instance,
                          value=request.data['value'],
                          ref_code=ref_code)
        serializer = self.get_serializer(data=deposit)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BeneficiaryBankModelViewSet(ModelViewSet):
    model = BeneficiaryBank
    serializer_class = BeneficiaryBankModelSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BeneficiaryBank.objects.filter(user=self.request.user)


class BeneficiaryMobileMoneyModelViewSet(ModelViewSet):
    model = BeneficiaryMobileMoney
    serializer_class = BeneficiaryMobileMoneyModelSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BeneficiaryMobileMoney.objects.filter(user=self.request.user)


class AdminWalletModelViewSet(ModelViewSet):
    model = Wallet
    serializer_class = WalletModelSerializer
    permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.all()

