from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)

from .models import Voucher


class VoucherModelSerializer(ModelSerializer):
    class Meta:
        model = Voucher
        fields = [
            'id',
            'pin',
            'business_unit',
            'currency',
            'used',
            'value',
        ]

        read_only_fields = (
            'id',
        )

