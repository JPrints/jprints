from django.db import models
from django.utils import timezone

from core.elastic_search import index_publication

class Milestone(models.Model):
    MILESTONE_TYPES = (
        ( 'D', 'Deposited' ),
        ( 'L', 'Live' ),
        ( 'A', 'Accepted' ),
        ( 'P', 'Published' ),
    )
 
    date = models.DateTimeField()
    milestone_type = models.CharField(max_length=1, choices=MILESTONE_TYPES)

class Contributor(models.Model):
    from core.models import Person

    CONTRIBUTION_TYPES = (
        ( 'Au', 'Author' ),
        ( 'Ed', 'Editor' ),
        ( 'Ad', 'Advisor' ),
        ( 'Re', 'Referee' ),
        ( 'Tr', 'TRANSLATOR' ),
    )
 
    contribution_type = models.CharField(max_length=2, choices=CONTRIBUTION_TYPES)
    person = models.ForeignKey(Person)

PUBLICATION_TYPES = (
        ( 'A', 'Article' ),
        ( 'B', 'Book' ),
        ( 'S', 'Book Section' ),
    )

DOCUMENT_TYPES = (
        ( 'dra', 'draft' ),
        ( 'sub', 'submitted' ),
        ( 'acc', 'accepted' ),
        ( 'pub', 'published' ),
        ( 'upd', 'updated' ),
        ( 'sup', 'supplemental' ),
        ( 'cov', 'coverimage' ),
        ( 'dat', 'dataset' ),
        ( 'pre', 'presentation' ),
        ( 'oth', 'other' ),
    )

LICENCES = (
        ( 'publi', 'publisher' ),
        ( 'cc_by', 'cc_by' ),
        ( 'by_nc', 'cc_by_nc' ),
        ( 'by_nd', 'cc_by_nd' ),
        ( 'nc_nd', 'cc_by_nc_nd' ),
        ( 'nc_sa', 'cc_by_nc_sa' ),
        ( 'by_sa', 'cc_by_sa' ),
        ( 'cc_pd', 'cc_public_domain' ),
    )

VISIBILITY_STATES = (
        ( 'P', 'Public' ),
        ( 'R', 'Restricted' ),
        ( 'E', 'Embagoed' ),
        ( 'N', 'None' ),
    )



class Publication(models.Model):
    from core.models import Person

    STATUS_TYPES = (
        ( 'I', 'inbox' ),
        ( 'B', 'buffer' ),
        ( 'A', 'archive' ),
        ( 'D', 'deletion' ),
    )

    PUBLICATION_STATES = (
        ( 'S', 'Submitted' ),
        ( 'A', 'Accepted' ),
        ( 'P', 'Published' ),
        ( 'I', 'In Press' ),
        ( 'U', 'Unpublished' ),
    )

    VISIBILITY_STATES = (
        ( 'P', 'Public' ),
        ( 'R', 'Restricted' ),
        ( 'E', 'Embagoed' ),
        ( 'N', 'None' ),
    )

    # metadata fields
    depositor = models.ForeignKey(Person)

    status = models.CharField(max_length=1, choices=STATUS_TYPES, default='I')
    publication_type = models.CharField(max_length=1, choices=PUBLICATION_TYPES, default='A')
    publication_status = models.CharField(max_length=1, choices=PUBLICATION_STATES, default='U')
    visibility_status = models.CharField(max_length=1, choices=VISIBILITY_STATES, default='N')
    title = models.CharField(max_length=200, blank=True)
    abstract = models.TextField(blank=True)

    #publication_date = models.DateField(null=True,auto_now=False,auto_now_add=False,blank=True)
    publication_date = models.DateField(auto_now=False,auto_now_add=False,blank=True)
    online_date = models.DateField(null=True,auto_now=False,auto_now_add=False,blank=True)
    accept_date = models.DateField(null=True,auto_now=False,auto_now_add=False,blank=True)
    submit_date = models.DateField(null=True,auto_now=False,auto_now_add=False,blank=True)
    complete_date = models.DateField(null=True,auto_now=False,auto_now_add=False,blank=True)

    subject = models.CharField(max_length=200, blank=True)
    divisions = models.CharField(max_length=200, blank=True)
    
    revision = models.IntegerField(default=1, editable=False)
    created = models.DateTimeField(auto_now_add=True, )
    #created = models.DateTimeField(auto_now_add=True, default=timezone.now(), editable=False)
    lastmod = models.DateTimeField(auto_now=True, blank=True, editable=False)

    def index(self):
        index_publication( self )

    # override the save method to index the object in elastic search
    def save(self, *args, **kwargs):
        super(Publication, self).save(*args, **kwargs) 
        index_publication( self )
        print("Publication.save called index !!!!!", self.id, self.title)

    def get_publication_type_str(self):
        type = ""
        if (self.publication_type):
            for t,n in PUBLICATION_TYPES:
                if ( t == self.publication_type ):
                    return n
        return type

    def get_search_citation(self):
        citation = self.title+" ["+self.get_publication_type_str()+"] "+self.abstract
        return citation

    def get_icon_name(self):
        icon_name = "research_books.png"
        if ( self.publication_type == "A" ):
            icon_name = "doc_file.png"
        elif ( self.publication_type == "B" ):
            icon_name = "research_books.png"
        elif ( self.publication_type == "S" ):
            icon_name = "research_books.png"

        return icon_name




    def __str__(self):
        return '%s %s' % (self.id, self.title)

class Document(models.Model):

    def pub_doc_path(instance, filename):
        return 'pub/{0}/doc/{1}/{2}'.format(instance.publication.id, instance.id, filename)

    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)

    doc_type = models.CharField(max_length=3, choices=DOCUMENT_TYPES, default='dra')
    visibility_status = models.CharField(max_length=1, choices=VISIBILITY_STATES, default='N')
    licence = models.CharField(max_length=5, choices=LICENCES, blank=True) 
    embargo = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, )
    filefield = models.FileField(upload_to=pub_doc_path, blank=True)





