# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from datetime import datetime
import uuid
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from orders.models import  BuyOrder
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from blockchain import exchangerates
from allauth.account.signals import user_signed_up
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.conf import settings
from wallet.models import Wallet
from cloudinary.models import CloudinaryField
from country.models import Country


class Level(models.Model):
    """
    user : Admin user who added or edited this level
    name : Name of this level
    discount: All users on this level enjoy this % discount
    limit: The maximum amount every user on this level can purchase monthly
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False)
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=100, null=True)
    id_number = models.CharField(max_length=20, null=True)
    verification_in_progress = models.BooleanField(default=False)
    verification_completed = models.BooleanField(default=False)
    verified_phone = models.BooleanField(default=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country')
    verification_declined = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def total_purchases(self):
        total = 0
        completed_orders = BuyOrder.objects.filter(user=self.id).filter(status="completed")
        if completed_orders:
            for order in completed_orders:
                total += order.amount_paid
        return total

    def orders_count(self):
        return BuyOrder.objects.filter(user=self.id).count()

    def new_users(self):
        today = datetime.date.today()
        new_users = User.objects.filter(date_joined__lte=today)
        return new_users


class Verification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name='user_verification')
    id_front = models.URLField(unique=False)
    id_number = models.CharField(max_length=20, null=True)
    id_back = models.URLField(unique=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    
class UserAnalytics(User):

    def new_users(self):
        today = datetime.datetime.today()
        new_users = User.objects.filter(date_joined=today)


class UserLoginHistory(models.Model):
    action = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name='user_login')
    ip = models.GenericIPAddressField(null=True, default='0.0.0.0')
    browser = models.CharField(max_length=256, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-time',)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):

    # if user does not have a wallet, create it for them
    if not Wallet.objects.filter(user=user).exists():
        user_wallet = Wallet(user=user, current_balance=0.00)
        user_wallet.save()

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')
    
    browser = request.META.get('HTTP_USER_AGENT')
    browser = str(browser)
    UserLoginHistory.objects.create(action='user_logged_in', ip=ipaddress, user=user, browser=browser)









