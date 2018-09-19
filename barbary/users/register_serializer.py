from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.conf import settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model, authenticate
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from wallet.models import Wallet
from country.models import Country
from .models import Level


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)  
    phone = serializers.CharField(required=False, write_only=True, min_length=10)

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'phone':  self.validated_data.get('phone', ''),
            'country':  self.validated_data.get('country', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        country_obj = Country.objects.get(id=request.data['country'])
        user.country = country_obj
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        """create wallet for user"""
        user_wallet = Wallet(user=user, current_balance=0.00, currency=country_obj.currency)
        user_wallet.save()
        return user

