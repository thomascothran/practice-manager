# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-13 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_auto_20160213_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='context',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]