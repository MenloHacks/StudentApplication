# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 03:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0035_remove_profile_application_reviewers'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='application_reviewers',
            field=models.ManyToManyField(blank=True, related_name='_profile_application_reviewers_+', to='application.Profile'),
        ),
    ]
