# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-19 16:50
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160818_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='values',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(null=True), size=None),
        ),
    ]