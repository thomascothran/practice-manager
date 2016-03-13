from django.conf.urls import url, include

from . import views

urlpatterns = [

    # Note urls
    # url(r'^note/(?P<pk>[a-zA-Z0-9_-]+)/details/$', views.NoteDetailView, name='note_details'),
    url(r'^note/create', views.CreateNoteView.as_view(), name='note_create'),
    url(r'^notes/$', views.NoteIndexView, name='note_index'),

]