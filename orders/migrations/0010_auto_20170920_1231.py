# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-20 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20170920_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellorder',
            name='account_name',
            field=models.CharField(max_length=30),
        ),
    ]
