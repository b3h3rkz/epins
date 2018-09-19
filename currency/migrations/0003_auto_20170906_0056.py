# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-06 00:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0002_auto_20170906_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'ACTIVE'), ('INACTIVE', 'INACTIVE'), ('OUT_OF_STOCK', 'OUT_OF_STOCK')], default='INACTIVE', max_length=10),
        ),
    ]