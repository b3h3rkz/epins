# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-16 00:59
from __future__ import unicode_literals
from django.db import migrations
from country.models import Country


def create_countries(apps, schema_editor):
    nigeria = Country(name="Nigeria", currency="NGN", iso_code="234")
    ghana = Country(name="Ghana", currency="GHS", iso_code="233")
    nigeria.save()
    ghana.save()


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0001_initial'),
    ]

    operations = [
        # migrations.RunPython(create_countries)
    ]
