from django.conf.urls import url


from . import views

app_name = 'api'
urlpatterns = [
    url(r'^lookup/contrib/$', views.lookup_person, name='lookup_person'),
]




