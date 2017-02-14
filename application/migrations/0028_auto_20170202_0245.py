# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-02 02:45
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0027_auto_20170126_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_campus_rep',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='zip_code',
            field=models.IntegerField(validators=[django.core.validators.RegexValidator(message=b"Zip code must be in the format '94027'. Only five numeric digits allowed.", regex=b'^\\d{5}$')]),
        ),
    ]