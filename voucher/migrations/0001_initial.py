# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-20 15:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business', '0001_initial'),
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('pin', models.CharField(max_length=16, unique=True)),
                ('used', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('business_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.BusinessUnit')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currency.Currency')),
            ],
        ),
    ]
