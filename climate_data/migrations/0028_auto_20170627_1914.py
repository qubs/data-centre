# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 19:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climate_data', '0027_remove_datatype_bounds'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datatype',
            old_name='bounds_2',
            new_name='bounds',
        ),
    ]