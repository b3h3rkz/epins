from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer

from .models import User, UserAnalytics, UserLoginHistory, Level
from wallet.serializers import WalletModelSerializer
from country.serializers import CountryModelSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class LevelModelSerializer(ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name', 'discount', 'limit',]


class UserAnalytics(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'new_users',
        ]


class UserLoginHistorySerializer(ModelSerializer):
    class Meta:
        model = UserLoginHistory
        fields = ['user', 'ip', 'browser', 'time']
        read_only_fields = ('user', 'ip', 'browser', 'time')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        user_login = UserLoginHistorySerializer(many=True, read_only=True)
        user_wallet = WalletModelSerializer(read_only=True)
        country = CountryModelSerializer(read_only=True)
        # level = LevelModelSerializer(read_only=True)
        depth = 1
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'country',
            'verified_phone',
            'verification_in_progress',
            'verification_completed',
            'user_login',
            'user_wallet',
            'phone',
            'date_joined',
            'last_login',
        ]
        read_only_fields = (
            'id',
            'password',

        )


class AdminUserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        user_login = UserLoginHistorySerializer(many=True, read_only=True)
        user_wallet = WalletModelSerializer(read_only=True )
        country = CountryModelSerializer(read_only=True)
        depth = 1
        fields = [
            'id',
            'username',
            'email',
            'verification_in_progress',
            'verification_completed',
            'user_wallet',
            'country',
            # 'verification_declined',
            # 'note',
            'is_staff',
            'user_login',
            'is_superuser',
            'is_active',
            'phone',
            'address',
            'date_joined',
            'first_name',
            'last_name',
            'last_login',
        ]
        read_only_fields = (
            'id',
            'password',

        )


class UsersModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()
