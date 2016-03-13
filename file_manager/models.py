from django.db import models
import uuid
from case_manager.models import Case
from people_and_property.models import Person
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from markupfield.fields import MarkupField
from django.conf import settings

# Create your models here.


class FileManagerTags(models.Model):
    """
    FileTags is the model for tags for files
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #user = models.ForeignKey(User)  # This is so each user can have different tags
                                                   # that shows up for them.
    name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name)

    # TO DO: Define get absolute url

# TO DO: Notebook model
    """
    The notebook model would disp
    """


class Note(models.Model):
    """
    Note is similar to an evernote note. It has a title, tags, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    title = models.CharField(max_length=60)
    note = MarkupField(null=True, blank=True)
    tags = models.ManyToManyField(FileManagerTags, related_name='tagged_note_set')
    cases = models.ManyToManyField(Case, related_name='related_note_set')
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='notes_user_can_edit'
    )
    viewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='notes_user_can_view',
        help_text='Who do you want to be able to view the note?'
    )

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('file_manager:note_create', kwargs={'pk': self.pk})



class FileObj(models.Model):
    """
    FileObj stores files of whatever type
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(help_text='Upload the file')
    name = models.CharField(help_text='Enter a name for the file', null=True, max_length=60)
    description = models.CharField(max_length=100, null=True)
    tags = models.ManyToManyField(FileManagerTags, related_name='tagged_files_set')
    cases = models.ManyToManyField(Case, related_name='related_files')
    person = models.ManyToManyField(Person, related_name='file_rel_to_person')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    # events = many files rel to events

    def __str__(self):
        return str(self.name) + str(self.id)

    # TO DO def get_absolute_url