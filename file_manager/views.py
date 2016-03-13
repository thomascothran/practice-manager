from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
from django.db.models import Q

from .models import Note

# Create your views here.


@login_required()
def NoteIndexView(request):
    """
    The note index view displays the notes. It should be able
    to be searched and to filter accordingly.
    """

    # TO DO: Set default note list
    note_list = Note.objects.filter(
        Q(creator=request.user)
    )

    if request.method == 'POST':
        return render(request, 'file_manager/note_index.html')
    else:
        return render(request, 'file_manager/note_index.html')


class CreateNoteView(PermissionRequiredMixin, CreateView):
    """
    This allows users to create notes
    """
    model = Note
    permission_required = 'file_manager.can_add_note'
    template_name = 'file_manager/note_create.html'
    fields = ['title', 'note', 'tags', 'cases', 'editors', 'viewers']

