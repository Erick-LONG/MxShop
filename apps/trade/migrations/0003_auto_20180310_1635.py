# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-10 08:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20180310_1625'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShopingCart',
            new_name='ShoppingCart',
        ),
    ]