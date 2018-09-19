from  .models import Country
from .serializers import CountryModelSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny


class CountryModelViewSet(ModelViewSet):
    model = Country
    serializer_class = CountryModelSerializer
    queryset = Country.objects.all()
    permission_classes = [AllowAny]

