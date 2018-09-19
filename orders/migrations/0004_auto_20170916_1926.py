# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-16 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20170911_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyorder',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='buyorder',
            name='network_name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='buyorder',
            name='transaction_id',
            field=models.CharField(default='', max_length=20),
        ),
    ]