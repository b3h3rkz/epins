# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-05 15:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verification',
            name='user',
        ),
        migrations.DeleteModel(
            name='Verification',
        ),
    ]
