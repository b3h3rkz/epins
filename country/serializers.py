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
from .models import Country


class CountryModelSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'iso_code', 'currency', 'active']
        read_only_fields = ['id', 'name', 'iso_code', 'currency', 'active']


class CountryAdminModelSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'iso_code', 'currency', 'active']
        read_only_fields = ['id', ]
