# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-20 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_sellorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellorder',
            name='amount_to_receive',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='sellorder',
            name='note',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='sellorder',
            name='tx_hash',
            field=models.CharField(default='', max_length=250),
        ),
    ]
