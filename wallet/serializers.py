from rest_framework import serializers
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
    CurrentUserDefault,
    ReadOnlyField,
    RelatedField,
    HiddenField, 
    PrimaryKeyRelatedField,
    HyperlinkedIdentityField
)
from .models import Wallet, Deposit, Withdrawal, BeneficiaryBank, BeneficiaryMobileMoney, ManualDeposit
from django.contrib.auth import get_user_model
import random
User = get_user_model()


class WalletModelSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
        fields = ['id',
                  'user',
                  'current_balance',
                  'created_at', ]


class BeneficiaryBankModelSerializer(ModelSerializer):
    class Meta:
        model = BeneficiaryBank
        user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
        fields = ['id',
                  'account_name',
                  'user',
                  'account_number',
                  'bank_branch',
                  'bank_name',
                  'created_at',
                  'modified', ]


class BeneficiaryMobileMoneyModelSerializer(ModelSerializer):
    class Meta:
        model = BeneficiaryMobileMoney
        user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
        fields = ['id',
                  'account_name',
                  'user',
                  'phone_number',
                  'provider',
                  'created_at',
                  'modified', ]


class DepositModelSerializer(ModelSerializer):
    class Meta:
        model = Deposit
        wallet = WalletModelSerializer(read_only=True)
        fields = ['id',
                  'value',
                  'created_at',
                  'modified', ]


class ManualDepositModelSerializer(ModelSerializer):
    class Meta:
        model = ManualDeposit
        user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
        fields = ['id',
                  'user',
                  'ref_code',
                  'status',
                  'method',
                  'value',
                  'created_at',
                  'modified', ]


class WithdrawalModelSerializer(ModelSerializer):
    class Meta:
        model = Withdrawal
        wallet = WalletModelSerializer(read_only=True)
        bank_account = BeneficiaryBankModelSerializer(read_only=True)
        momo_account = BeneficiaryMobileMoneyModelSerializer(read_only=True)
        fields = ['id',
                  'wallet',
                  'value',
                  'status',
                  'bank_account',
                  'momo_account',
                  'created_at',
                  'modified', ]



