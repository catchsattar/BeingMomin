# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-26 11:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AmbassadorPortal', '0002_auto_20190426_0556'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='locality_mapping',
            table='AmbassadorPortal_locality_mapping',
        ),
        migrations.AlterModelTable(
            name='people',
            table='AmbassadorPortal_people',
        ),
    ]
