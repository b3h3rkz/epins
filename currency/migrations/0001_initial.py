# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-12 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('symbol', models.CharField(max_length=3, unique=True)),
                ('logo', models.ImageField(blank=True, upload_to='')),
                ('buy_rate', models.DecimalField(decimal_places=2, max_digits=3)),
                ('sell_rate', models.DecimalField(decimal_places=2, max_digits=3)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default=0, max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
