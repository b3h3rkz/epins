# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-22 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_auto_20171122_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyorder',
            name='amount_paid',
            field=models.DecimalField(decimal_places=3, max_digits=10, null=True),
        ),
    ]
