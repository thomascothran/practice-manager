# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-13 21:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import markupfield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('case_manager', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people_and_property', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileObj',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(help_text='Upload the file', upload_to='')),
                ('name', models.CharField(help_text='Enter a name for the file', max_length=60, null=True)),
                ('description', models.CharField(max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('cases', models.ManyToManyField(related_name='related_files', to='case_manager.Case')),
                ('person', models.ManyToManyField(related_name='file_rel_to_person', to='people_and_property.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=60)),
                ('note', markupfield.fields.MarkupField(blank=True, null=True, rendered_field=True)),
                ('note_markup_type', models.CharField(blank=True, choices=[('', '--'), ('html', 'HTML'), ('plain', 'Plain'), ('markdown', 'Markdown')], default=None, max_length=30, null=True)),
                ('_note_rendered', models.TextField(editable=False, null=True)),
                ('cases', models.ManyToManyField(related_name='related_note_set', to='case_manager.Case')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('editors', models.ManyToManyField(related_name='notes_user_can_edit', to=settings.AUTH_USER_MODEL)),
                ('viewers', models.ManyToManyField(help_text='Who do you want to be able to view the note?', related_name='notes_user_can_view', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
