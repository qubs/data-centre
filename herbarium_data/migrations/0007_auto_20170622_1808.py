# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-22 18:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herbarium_data', '0006_auto_20170622_1805'),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER common_name SET DEFAULT ''"),
    ]