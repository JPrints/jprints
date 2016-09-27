from django.test import TestCase


from .models import Publication

class PublicationMethodTest(TestCase):

    def test_publication_has_status(self):
        """
        publication must have a valid status
        """
        pub = Publication()
        self.assertIs(pub.status, 'I')

