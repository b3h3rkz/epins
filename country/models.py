from django.db import models
import uuid


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, unique=True)
    currency = models.CharField(max_length=3, unique=True)
    iso_code = models.CharField(max_length=3, unique=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

#
# class Bank(models.Model):
#     """
#      List of Supported Banks we make payments to
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=20, unique=True)
#     country = models.OneToOneField(Country, on_delete=models.CASCADE, related_name='bank_country')
#     active = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name
#
#
# class MobileNetwork(models.Model):
#     """
#      List of Supported Mobile Money Merchants we make payments to
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=20, unique=True)
#     country = models.OneToOneField(Country, on_delete=models.CASCADE, related_name='mobilemoney_country')
#     active = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name




