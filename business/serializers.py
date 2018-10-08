from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    CurrentUserDefault
)

from .models import BusinessUnit


class BusinessUnitUserSerializer(ModelSerializer):
    merchant = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

    class Meta:
        model = BusinessUnit
        fields = [
            'id',
            'merchant',
            'name',
            'website_url',
            'logo_url',
            'voucher_length',
        ]
        read_only_fields = (
            'id',
        )


class BusinessUnitSerializer(ModelSerializer):

    class Meta:
        model = BusinessUnit
        fields = [
            'id',
            'name',
            'website_url',
            'logo_url',
            'voucher_length'
        ]
        read_only_fields = [
            'id',
            'name',
            'website_url',
            'logo_url',
            'voucher_length'
        ]
