import json
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
)

from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .serializers import CurrencyModelSerializer, CurrencyPublicModelSerializer
from .models import Currency

"""
Todos
1. set permissions for who can update rates
2.keep track of rates history
"""


class CurrencyModelViewSet(ModelViewSet):
    model = Currency
    queryset = Currency.objects.all()
    serializer_class = CurrencyModelSerializer
    # permission_classes = [IsAuthenticated]

    # @list_route(permission_classes=[AllowAny], methods=['get'], serializer_class=CurrencyModelSerializer)
    # def get_currencies(self, request, pk=None):
    #     currency = Currency.objects.all()
    #     currency_unicode = request.body.decode('utf-8')
    #     return Response()


class CurrencyPublicListModelViewSet(ModelViewSet):
    """
     Show currency
    """
    model = Currency
    queryset = Currency.objects.all()
    serializer_class = CurrencyPublicModelSerializer




