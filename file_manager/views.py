from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Note

# Create your views here.


class NoteIndexView(PermissionRequiredMixin, ListView):
    permission_required = 'file_manager.can_change_note'
    template_name = 'file_manager/note_index.html'
    model = Note


class CreateNoteView(PermissionRequiredMixin, CreateView):
    """
    This allows users to create notes
    """
    model = Note
    permission_required = 'file_manager.can_add_note'
    template_name = 'file_manager/note_create.html'
    fields = ['title', 'note', 'tags', 'cases', 'people']




