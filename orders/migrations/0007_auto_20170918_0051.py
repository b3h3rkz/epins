# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-18 00:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20170918_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyorder',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]
