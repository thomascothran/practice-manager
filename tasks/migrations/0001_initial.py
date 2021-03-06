# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 21:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('case_manager', '0001_initial'),
        ('people_and_property', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('purpose', models.TextField(blank=True)),
                ('vision', models.TextField(blank=True)),
                ('big_steps', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('complete', 'complete')], default='pending', max_length=30)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('context', models.CharField(choices=[('@work', '@work'), ('@home', '@home'), ('@town', '@town'), ('@philosophy', '@philosophy')], max_length=50)),
                ('priority', models.CharField(choices=[('1-Now', '1-Now'), ('2-Next', '2-Next'), ('3-Soon', '3-Soon'), ('4-Later', '4-Later'), ('5-Even Later', '5-Even Later'), ('6-Someday/Maybe', '6-Someday/Maybe'), ('7-Waiting', '7-Waiting'), ('8-In Queu', '8-In Queau'), ('9-On Hold', '9-On Hold')], max_length=50)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_assigned_to', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_created_by', to=settings.AUTH_USER_MODEL)),
                ('related_cases', models.ManyToManyField(related_name='projects_rel_to_case', to='case_manager.Case')),
                ('related_persons', models.ManyToManyField(related_name='projects_rel_to_person', to='people_and_property.Person')),
                ('related_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.Project')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_supervisor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('complete', 'complete')], default='pending', max_length=30)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('context', models.CharField(choices=[('@work', '@work'), ('@home', '@home'), ('@town', '@town'), ('@philosophy', '@philosophy')], max_length=50)),
                ('priority', models.CharField(choices=[('1-Now', '1-Now'), ('2-Next', '2-Next'), ('3-Soon', '3-Soon'), ('4-Later', '4-Later'), ('5-Even Later', '5-Even Later'), ('6-Someday/Maybe', '6-Someday/Maybe'), ('7-Waiting', '7-Waiting'), ('8-In Queu', '8-In Queau'), ('9-On Hold', '9-On Hold')], max_length=50)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_assigned_to', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_created_by', to=settings.AUTH_USER_MODEL)),
                ('related_cases', models.ManyToManyField(related_name='tasks_rel_to_case', to='case_manager.Case')),
                ('related_persons', models.ManyToManyField(related_name='tasks_rel_to_person', to='people_and_property.Person')),
                ('related_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.Project')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_supervisor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
