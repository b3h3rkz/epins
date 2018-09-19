# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-17 07:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20170916_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyorder',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='currency', to='currency.Currency'),
        ),
    ]
