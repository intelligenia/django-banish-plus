# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-19 14:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banish', '0002_auto_20170826_1311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banishment',
            options={'permissions': (('can_ban_user', 'Can Ban User'),), 'verbose_name': 'Banishment Blacklist', 'verbose_name_plural': 'Banishments Blacklist'},
        ),
        migrations.AlterModelOptions(
            name='whitelist',
            options={'permissions': (('can_whitelist_user', 'Can Whitelist User'),), 'verbose_name': 'Banishment Whitelist', 'verbose_name_plural': 'Banishments Whitelist'},
        ),
    ]
