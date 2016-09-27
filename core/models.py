from django.db import models
from django.contrib.auth.models import User

class Permission(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return '%s %s' % (self.id, self.name)

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return '%s %s' % (self.id, self.name)

class Person(models.Model):

    USER_TYPES = (
        ( 'Ad', 'Admin' ),
        ( 'Ed', 'Editor' ),
        ( 'Us', 'User' ),
        ( 'Gu', 'Guest' ),
        ( 'Ex', 'External' ),
    )
    USER_LANG = (
        ( 'EN', 'English' ),
        ( 'DE', 'Duetsch' ),
        ( 'FR', 'Français' ),
        ( 'IT', 'Italiano' ),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_images', blank=True)
    disp_title = models.CharField(max_length=20, blank=True)
    disp_given = models.CharField(max_length=50, blank=True)
    disp_family = models.CharField(max_length=50, blank=True)
    lang = models.CharField(max_length=2, choices=USER_LANG, blank=True)
    orcid = models.CharField(max_length=20, blank=True)
    user_type = models.CharField(max_length=2, choices=USER_TYPES)
    dept = models.CharField(max_length=100, blank=True)
    org = models.CharField(max_length=100, blank=True)
    addr = models.CharField(max_length=100, blank=True)
    roles = models.ManyToManyField(Role, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    lastmod = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.id, self.user)


class SavedSearch(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    detail = models.CharField(max_length=200, blank=True)


    def __str__(self):
        return '%s %s' % (self.id, self.name)



