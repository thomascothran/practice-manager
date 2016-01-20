from django.conf.urls import url, include

from . import views

urlpatterns = [

    # url(r'^note/(?P<pk>[a-zA-Z0-9_-]+)/details/$', views.NoteDetailView, name='note_details'),
    url(r'^note/create', views.CreateView, name='note_create'),

]