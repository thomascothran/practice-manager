from django.db import models
import uuid
from case_manager.models import Case
from people_and_property.models import Person
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from markupfield.fields import MarkupField
from django.conf import settings

# Create your models here.

class Notebook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(max_length=60)
    description = MarkupField(blank=True, markup_type='markdown')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='owned_notebooks'
    )
    viewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='viewable_notebooks')
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='editable_notebooks'
    )

    def __str__(self):
        return self.name

    # TO DO: Define an absolute url



class Note(models.Model):
    """
    Note is similar to an evernote note. It has a title, tags, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    title = models.CharField(max_length=60)
    note = MarkupField(null=True, blank=True, markup_type='markdown')
    cases = models.ManyToManyField(Case, related_name='related_note_set', blank=True)
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='notes_user_can_edit',
        blank=True
    )
    viewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='notes_user_can_view',
        help_text='Who do you want to be able to view the note?',
        blank=True
    )
    notebook = models.ForeignKey(
        Notebook,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('file_manager:note_detail', kwargs={'pk': self.pk})



class FileObj(models.Model):
    """
    FileObj stores files of whatever type
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(help_text='Upload the file')
    name = models.CharField(help_text='Enter a name for the file', null=True, max_length=60)
    description = models.CharField(max_length=100, null=True)
    cases = models.ManyToManyField(Case, related_name='related_files')
    person = models.ManyToManyField(Person, related_name='file_rel_to_person')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    # events = many files rel to events

    def __str__(self):
        return str(self.name) + str(self.id)

    # TO DO:    def get_absolute_url(self):
