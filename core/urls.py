from django.conf.urls import url


from . import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^edit/(?P<profileid>[0-9]+)/$', views.edit_profile, name='edit_profile'),
    url(r'^profiles/$', views.profiles, name='profiles'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^search/$', views.search, name='search'),
    url(r'^filter/(?P<ftype>[\w]+)/(?P<ffield>[\w]+)/$', views.filter, name='filter'),
    url(r'^browse/(?P<ftype>[\w]+)/$', views.browse, name='browse'),
    url(r'^browse/(?P<ftype>[\w]+)/bibliograpy/$', views.browse_bibliography, name='bibliograpy'),
    #url(r'^browse/$', views.browse, name='browse_top'),
]


