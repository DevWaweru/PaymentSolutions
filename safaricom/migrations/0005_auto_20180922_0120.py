# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-21 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safaricom', '0004_successfultransfer_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unsuccessfultransfer',
            name='result_description',
            field=models.CharField(max_length=150),
        ),
    ]
