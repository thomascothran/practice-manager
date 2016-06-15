from django.conf.urls import url, include

from . import views

urlpatterns = [

    # Note urls
    url(r'^note/(?P<pk>[a-zA-Z0-9_-]+)/details/$', views.NoteDetailView.as_view(), name='note_details'),
    url(r'^note/create', views.CreateNoteView.as_view(), name='note_create'),
    url(r'^notes/$', views.NoteIndexView, name='note_index'),
    # url(r'^note/update/(?P<pk>[a-zA-Z0-9_-]+)$', views.NoteUpdateView.as_view(), name='note_update')

]