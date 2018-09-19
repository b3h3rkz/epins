# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-01-28 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_auto_20180121_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyorder',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency', to='currency.Currency'),
        ),
    ]