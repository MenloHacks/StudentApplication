# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-26 23:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0011_application_form_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='can_bring_chaperone',
            field=models.BooleanField(default=False),
        ),
    ]
