# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-22 17:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('herbarium_data', '0004_auto_20170622_1746'),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER dataset SET DEFAULT ''"),
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER genus SET DEFAULT ''"),
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER species SET DEFAULT ''"),
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER common_name SET DEFAULT ''"),
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER dth SET DEFAULT ''"),
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER collectors SET DEFAULT ''"),
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER map_reference SET DEFAULT ''"),
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER county SET DEFAULT ''"),
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER township SET DEFAULT ''"),
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER country SET DEFAULT ''"),
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER location SET DEFAULT ''"),
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER habitat SET DEFAULT ''"),
        migrations.RunSQL("ALTER TABLE herbarium_data_specimen ALTER notes SET DEFAULT ''"),
    ]