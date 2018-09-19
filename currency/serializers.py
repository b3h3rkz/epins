from rest_framework.serializers import HyperlinkedModelSerializer, RelatedField, ModelSerializer
from .models import Currency


class CurrencyModelSerializer(ModelSerializer):

    class Meta:
        model = Currency
        lookup_field = 'pk'
        fields = (
            'name',
            'symbol',
            'buy_rate',
            'sell_rate',
            'status',
            'fees',
            'logo',
            'slug',
            'id',
            'created',
            'modified'
        )


class CurrencyPublicModelSerializer(ModelSerializer):

    class Meta:
        model = Currency
        lookup_field = 'pk'
        fields = (
            'name',
            'symbol',
            'logo',
            'slug',
            'price',
            'id',
            'created',
            'modified'
        )