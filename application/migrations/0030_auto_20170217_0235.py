# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 02:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0029_merge_20170217_0234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationreview',
            name='adjusted_score',
        ),
        migrations.RemoveField(
            model_name='applicationreview',
            name='score',
        ),
        migrations.AddField(
            model_name='application',
            name='cumulative_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='applicationreview',
            name='adjusted_experience_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='applicationreview',
            name='adjusted_passion_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='applicationreview',
            name='experience_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='applicationreview',
            name='form_ok',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='applicationreview',
            name='passion_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='applicationreview',
            name='photo_form_ok',
            field=models.BooleanField(default=False),
        ),
    ]