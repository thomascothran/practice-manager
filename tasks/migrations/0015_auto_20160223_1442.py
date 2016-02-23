# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-23 19:42
from __future__ import unicode_literals

from django.db import migrations, models
import markupfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_auto_20160213_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='context',
            name='_description_rendered',
            field=models.TextField(default='', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='context',
            name='description_markup_type',
            field=models.CharField(choices=[('', '--'), ('html', 'HTML'), ('plain', 'Plain'), ('markdown', 'Markdown')], default='markdown', editable=False, max_length=30),
        ),
        migrations.AlterField(
            model_name='context',
            name='description',
            field=markupfield.fields.MarkupField(blank=True, rendered_field=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('complete', 'complete'), ('any', 'any')], default='pending', max_length=30),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('complete', 'complete'), ('any', 'any')], default='pending', max_length=30),
        ),
    ]
