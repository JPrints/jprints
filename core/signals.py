from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from core.models import Person
from core.elastic_search import rm_index_person
import shutil



@receiver(pre_delete, sender=Person, dispatch_uid='person_delete_signal')
def tidy_up_profile(sender, instance, using, **kwargs):
    if instance.photo and instance.id :
        instance.photo.delete()
        try:
            profile_path = settings.MEDIA_DIR + "/profile/" +str(instance.id)
            shutil.rmtree(profile_path)
        except:
            print("tidy_up_profile exception raised")

        rm_index_person(instance)

 


