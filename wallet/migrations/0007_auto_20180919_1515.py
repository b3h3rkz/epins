# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-19 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0006_auto_20180919_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manualdeposit',
            name='ref_code',
            field=models.CharField(default='BTBY0EUGI', editable=False, max_length=250),
        ),
    ]
