# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-26 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20160125_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='under_projects',
            field=models.ManyToManyField(blank=True, related_name='subordinate_projects', to='tasks.Project'),
        ),
    ]
