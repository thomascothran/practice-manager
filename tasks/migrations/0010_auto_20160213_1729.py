# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-13 22:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_auto_20160129_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='related_cases',
            field=models.ManyToManyField(blank=True, related_name='projects_rel_to_case', to='case_manager.Case'),
        ),
        migrations.AlterField(
            model_name='project',
            name='related_persons',
            field=models.ManyToManyField(blank=True, related_name='projects_rel_to_person', to='people_and_property.Person'),
        ),
        migrations.AlterField(
            model_name='task',
            name='related_cases',
            field=models.ManyToManyField(blank=True, related_name='tasks_rel_to_case', to='case_manager.Case'),
        ),
        migrations.AlterField(
            model_name='task',
            name='related_persons',
            field=models.ManyToManyField(blank=True, related_name='tasks_rel_to_person', to='people_and_property.Person'),
        ),
    ]