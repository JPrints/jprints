from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
from publications.models import Publication, Document
from core.elastic_search import rm_index_publication
import shutil


@receiver(pre_delete, sender=Publication, dispatch_uid='publication_delete_signal')
def tidy_up_publication(sender, instance, using, **kwargs):
    documents = Document.objects.filter(publication__id = instance.id)
    doc_count = 0
    for fulltext in documents:
        if fulltext.filefield:
            fulltext.filefield.delete()
            doc_count += 1

    if doc_count > 0:
        try:
            doc_path = settings.MEDIA_DIR + "/pub/" +str(instance.id)
            shutil.rmtree(doc_path)
        except:
            print("tidy_up_publication exception raised")

    rm_index_publication(instance)
 


