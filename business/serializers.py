from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    CurrentUserDefault
)

from .models import BusinessUnit


class BusinessUnitModelSerializer(ModelSerializer):
    merchant = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    class Meta:
        model = BusinessUnit
        fields = [
            'merchant',
            'name',
            'website_url',
            'logo_url',
            'voucher_length',
        ]
