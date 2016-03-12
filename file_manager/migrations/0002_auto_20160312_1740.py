# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-12 22:40
from __future__ import unicode_literals

from django.db import migrations, models
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='_note_rendered',
            field=models.TextField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='note_markup_type',
            field=models.CharField(blank=True, choices=[('', '--'), ('html', 'HTML'), ('plain', 'Plain'), ('markdown', 'Markdown')], default=None, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='note',
            field=markupfield.fields.MarkupField(blank=True, null=True, rendered_field=True),
        ),
    ]
