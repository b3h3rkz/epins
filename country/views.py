from  .models import Country
from .serializers import CountryModelSerializer, CountryAdminModelSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny


class CountryModelViewSet(ModelViewSet):
    model = Country
    serializer_class = CountryModelSerializer
    queryset = Country.objects.all()
    permission_classes = [AllowAny]


class CountryAdminModelViewSet(ModelViewSet):
    model = Country
    serializer_class = CountryAdminModelSerializer
    queryset = Country.objects.all()
    permission_classes = [IsAdminUser]
