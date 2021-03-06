# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-23 22:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaypalTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100)),
                ('payer_id', models.CharField(max_length=100)),
                ('payment_id', models.CharField(max_length=100)),
                ('nonce', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
