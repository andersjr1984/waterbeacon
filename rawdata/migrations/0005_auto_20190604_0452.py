# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-06-04 04:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rawdata', '0004_auto_20190604_0433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epafacilitysystem',
            name='RegistryID',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
