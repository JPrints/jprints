from django.db import models
from django.contrib.auth.models import User
from core.elastic_search import index_person

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

    def profile_photo_path(instance, filename):
        return 'profile/{0}/photo/{1}'.format(instance.user.id, filename)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=profile_photo_path, blank=True)
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

    def index(self):
        print("Person.index calling index !!!!!")
        index_person( self )
 
    def render_name(self):
        name = self.disp_title+", "+self.disp_given+" "+self.disp_family
        return name

    def get_search_citation(self):
        citation = self.disp_title+", "+self.disp_given+" "+self.disp_family
        if ( self.orcid):
            citation += " ("+ self.orcid+")"
        return citation



    # override the save method to index the object in elastic search
    def save(self, *args, **kwargs):
        super(Person, self).save(*args, **kwargs) 
        if len(self.disp_given) == 0 :
           self.disp_given = self.user.first_name

        if len(self.disp_family) == 0 :
           self.disp_family = self.user.last_name

        index_person( self )
        #print("person.save called index !!!!!", self.id, self.user.last_name)


    def __str__(self):
        return '%s %s' % (self.id, self.user)


class SavedSearch(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    detail = models.CharField(max_length=200, blank=True)


    def __str__(self):
        return '%s %s' % (self.id, self.name)



