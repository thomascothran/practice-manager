from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls
from . import views

urlpatterns = [
    # Index
    url(r'^$', views.IndexView, name='index'),
    url(r'^create-new-client$', views.CreateNewClient, name='create-new-client'),
    url(r'^case/(?P<pk>[a-zA-Z0-9_-]+)/details/$', views.CaseDetailView.as_view(), name='case-detail'),
    url(r'^case/create/$', views.CreateCaseView.as_view(), name='case_create'),
    url(r'^case/(?P<pk>[a-zA-Z0-9_-]+)/update/$', views.UpdateCaseView.as_view(), name='case_update'),
    url(r'^client-list/$', views.ClientListView, name='client_index')

]