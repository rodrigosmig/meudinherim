# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-09 22:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contas_a_pagar', '0005_auto_20190209_1230'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contasapagar',
            old_name='data_vencimento',
            new_name='data',
        ),
    ]
