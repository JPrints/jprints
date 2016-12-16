from django.conf.urls import url

from . import views

app_name = 'publication'
urlpatterns = [
#    url(r'^$', views.index, name='index'),
#    url(r'^(?P<pub_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/detail$', views.detail, name='detail'),
    url(r'^add_publication/$', views.add_publication, name='add_publication'),
    url(r'^edit/(?P<pubid>[0-9]+)/$', views.edit_publication, name='edit_publication'),
    url(r'^add_doc/(?P<pubid>[0-9]+)/$', views.add_doc, name='add_document'),
]


