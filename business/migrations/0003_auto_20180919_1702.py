# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-19 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_auto_20180919_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessunit',
            name='website_url',
            field=models.URLField(max_length=120, null=True),
        ),
    ]
