# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 19:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0015_auto_20161123_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='file_upload',
        ),
    ]
