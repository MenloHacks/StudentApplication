# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 04:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_hackathons', models.CharField(choices=[(b'0', b'0'), (b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4+', b'4+')], max_length=2)),
                ('cool_project', models.TextField()),
                ('last_summer', models.TextField()),
                ('anything_else', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('school', models.CharField(max_length=150)),
                ('zip_code', models.IntegerField()),
                ('github_profile', models.URLField()),
                ('linkedin_profile', models.URLField()),
                ('devpost_profile', models.URLField()),
                ('personal_website', models.URLField()),
                ('dietary_restrictions', models.CharField(choices=[(b'None', b'None'), (b'Vegetarian', b'Vegetarian'), (b'Vegan', b'Vegan'), (b'Gluten Free', b'Gluten Free')], max_length=15)),
                ('t_shirt_size', models.CharField(choices=[(b'XS', b'XS'), (b'S', b'S'), (b'M', b'M'), (b'L', b'L'), (b'XL', b'XL')], max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='application.Profile'),
        ),
    ]
