# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-09 14:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas_a_pagar', '0004_auto_20171222_1111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contasapagar',
            old_name='data',
            new_name='data_vencimento',
        ),
        migrations.AddField(
            model_name='contasapagar',
            name='data_pagamento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
