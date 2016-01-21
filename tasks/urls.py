from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls
from . import views

urlpatterns = [
    # Index
    url(r'^$', views.IndexView, name='index'),

    # Login/Logout/Change Password/Etc
    url(r'^settings/$', views.settings, name='settings'),

    # TASKS
    # E.g., /task/3j243o-Ofjdsof-3123
    url(r'^tasks/(?P<pk>[0-9a-zA-Z_-]+)/$', views.TaskDetailView.as_view(), name='task_detail'),
    # Adding tasks
    url(r'^add-task/$', views.TaskCreate.as_view(), name='add_task'),
    # Update/view tasks
    url(r'^view-task/(?P<pk>[0-9a-zA-Z_-]+)/$', views.TaskUpdate.as_view(), name='view_task'),

    # PROJECTS
    # E.g., /project/234jf0we-324skl-34j
    url(r'^projects/(?P<pk>[a-zA-Z0-9_-]+)/$', views.ProjectDetailView.as_view(), name='project_detail'),
    # Adding projects
    url(r'^add-project/$', views.ProjectCreate.as_view(), name='add_project'),
    # Updating/viewing Projects
    url(r'^update-project/(?P<pk>[a-zA-Z0-9_-]+)/$', views.ProjectUpdate.as_view(), name='update-project'),

    # TAGS
    url(r'^context/add/$', views.ContextTagCreate.as_view(), name='context_add'),

]