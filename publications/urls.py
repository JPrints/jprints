from django.conf.urls import url

from . import views

app_name = 'publication'
urlpatterns = [
#    url(r'^$', views.index, name='index'),
#    url(r'^(?P<pub_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/detail$', views.mydetail, name='mydetail'),
    url(r'^add_publication/$', views.add_publication, name='add_publication'),
]


