from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class BusinessUnit(models.Model):
    merchant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    website_url = models.URLField(max_length=120, null=True)
    logo_url = models.URLField(max_length=250)
    voucher_length = models.IntegerField(default=0)

    def __str__(self):
        return self.name
