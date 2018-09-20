from django.db import models
from django.conf import settings

from business.models import BusinessUnit
from currency.models import Currency

class Voucher(models.Model):
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    pin = models.CharField(max_length=16, unique=True)
    used = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pin)
