from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED

from barbary.users.models import User
from .models import BusinessUnit
from .serializers import BusinessUnitModelSerializer


class BusinessUnitViewset(ModelViewSet):
    model = BusinessUnit
    serializer_class = BusinessUnitModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BusinessUnit.objects.filter(merchant=self.request.user.id)
