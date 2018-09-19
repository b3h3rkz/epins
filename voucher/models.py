from django.db import models

# Create your models here.


class Voucher(models.Model):
    pin = models.CharField(max_length=10, unique=True)
    used = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.used