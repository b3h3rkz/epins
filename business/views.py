from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.response import Response
from rest_framework import status

from barbary.users.models import User
from .models import BusinessUnit
from .serializers import BusinessUnitSerializer, BusinessUnitUserSerializer


class BusinessUnitUserViewset(ModelViewSet):
    model = BusinessUnit
    serializer_class = BusinessUnitUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BusinessUnit.objects.filter(merchant=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK, headers=self.get_success_headers(serializer.data))


class BusinessUnitViewset(ModelViewSet):
    model = BusinessUnit
    serializer_class = BusinessUnitSerializer
    queryset = BusinessUnit.objects.all()
    permission_classes = [AllowAny]
