# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-23 15:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('safaricom', '0005_auto_20180922_0120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='successfultransfer',
            options={'ordering': ('-id',)},
        ),
    ]