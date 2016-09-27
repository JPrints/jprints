from django.db import models
from django.utils import timezone

from core.models import Person

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


class Publication(models.Model):
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



    depositor = models.ForeignKey(Person)

    status = models.CharField(max_length=1, choices=STATUS_TYPES, default='I')
    publication_type = models.CharField(max_length=1, choices=PUBLICATION_TYPES, default='A')
    publication_status = models.CharField(max_length=1, choices=PUBLICATION_STATES, default='U')
    visibility_status = models.CharField(max_length=1, choices=VISIBILITY_STATES, default='N')
    title = models.CharField(max_length=200, blank=True)
    abstract = models.TextField(blank=True)

    subject = models.CharField(max_length=200, blank=True)
    divisions = models.CharField(max_length=200, blank=True)
    

    revision = models.IntegerField(default=1, editable=False)
    created = models.DateTimeField(auto_now_add=True, )
    #created = models.DateTimeField(auto_now_add=True, default=timezone.now(), editable=False)
    lastmod = models.DateTimeField(auto_now=True, blank=True, editable=False)


    def __str__(self):
        return '%s %s' % (self.id, self.title)


