from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls
from . import views

urlpatterns = [
    # url(r'^$', views.IndexView, name='index'),
    url(r'^person/(?P<pk>[a-zA-Z0-9_-]+)/details/$', views.PersonDetail.as_view(), name='person-detail'),
    url(r'^person/(?P<pk>[a-zA-Z0-9_-]+)/edit/$', views.PersonUpdate.as_view(), name='person-update'),
    url(r'^person/create/$', views.PersonCreate.as_view(), name='person-create'),
    url(r'^email/(?P<pk>[a-zA-Z0-9_-]+)/details', views.EmailDetail.as_view(), name='email-detail'),
    url(r'^email/create/$', views.EmailCreate.as_view(), name='email-create'),
    url(r'^email/(?P<pk>[a-zA-Z0-9_-]+)/edit/$', views.EmailUpdate.as_view(), name='email_update'),
    url(r'^phone/(?P<pk>[a-zA-Z0-9_-]+)/details/$', views.PhoneDetail.as_view(), name='phone_detail'),
    url(r'^phone/create/$', views.PhoneCreate.as_view(), name='phone_create'),
    url(r'^phone/(?P<pk>[a-zA-Z0-9_-]+)/edit/$', views.PhoneUpdate.as_view(), name='phone_update'),
    url(r'^fax/create/$', views.FaxCreate.as_view(), name='fax_create'),
    url(r'^fax/(?P<pk>[a-zA-Z0-9_-]+)/edit/$', views.FaxUpdate.as_view(), name='fax_update'),
    url(r'^fax/(?P<pk>[a-zA-Z0-9_-]+)/details/$', views.FaxDetail.as_view(), name='fax_detail'),
    url(r'^address/(?P<pk>[a-zA-Z0-9_-]+)/details/$', views.AddressDetail.as_view(), name='address_detail'),
    url(r'^address/(?P<pk>[a-zA-Z0-9_-]+)/update/$', views.AddressUpdate.as_view(), name='address_update'),
    url(r'^address/create/$', views.AddressCreate.as_view(), name='address_create'),

]