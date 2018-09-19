from django.db import models
from django.template.defaultfilters import slugify
import requests

class Currency(models.Model):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    OUT_OF_STOCK = 'OUT_OF_STOCK'
    CURRENCY_STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
        (OUT_OF_STOCK, 'OUT_OF_STOCK'),
    )

    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)
    symbol = models.CharField(max_length=3, unique=True)
    logo = models.URLField(blank=False, unique=True)
    buy_rate = models.DecimalField(decimal_places=2, max_digits=3)
    sell_rate = models.DecimalField(decimal_places=2, max_digits=3)
    fees = models.DecimalField(decimal_places=2, max_digits=16, default=0.00)
    status = models.CharField(max_length=10, choices=CURRENCY_STATUS_CHOICES, default=INACTIVE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def slug(self):
        return slugify(self.name)

    def price(self):
        url = "https://blockchain.info/tobtc"
        params = {
            "currency": 'USD',
            "value": self.buy_rate
        }
        price = requests.get(url, params=params)
        return price.text

