from django import forms

from .models import Milestone, Contributor, Publication, Document, DOCUMENT_TYPES, LICENCES, VISIBILITY_STATES
from core.models import Person

#class PublicationFormDepositor(forms.ModelForm):
#
#    def __init__(self, person):
#        self.person = person
#        print(person)
#        super().__init__()
#
#    publication_type = forms.CharField(
#        max_length=1,
#        widget=forms.Select(choices=Publication.PUBLICATION_TYPES),
#        help_text="Please enter the Publication Type")
#    title = forms.CharField(max_length=200, help_text="title")
#    abstract = forms.CharField(help_text="abstract", 
#        widget=forms.Textarea(),
#        required=False)
#    subject = forms.CharField(max_length=200, help_text="The subjects")
#    divisions = forms.CharField(max_length=200, help_text="divisions")
#
#    status = forms.CharField(widget=forms.HiddenInput(), initial='I')
#    publication_status = forms.CharField(widget=forms.HiddenInput(), initial='U')
#    visibility_status = forms.CharField(widget=forms.HiddenInput(), initial='N')
#    revision = forms.IntegerField(widget=forms.HiddenInput(), initial='1')
#
#    class Meta:
#        model = Publication
#        fields = ( 'publication_type', 'title', 'abstract', 'subject', 'divisions')

class PublicationForm(forms.ModelForm):

    depositor = forms.ModelChoiceField(queryset=Person.objects.all(), help_text="Depositor", empty_label="Deposit on behalf of")
    #contributors = forms.ModelMultipleChoiceField(queryset=Person.objects.all(), help_text="Contributors", required=False)
    publication_type = forms.CharField(
        max_length=1,
        widget=forms.Select(choices=Publication.PUBLICATION_TYPES),
        help_text="Please enter the Publication Type")
    title = forms.CharField(max_length=200, help_text="title", widget=forms.TextInput(attrs={'size': 40}))
    abstract = forms.CharField(help_text="abstract", 
        widget=forms.Textarea(),
        required=False)
    subject = forms.CharField(max_length=200, help_text="The subjects")
    divisions = forms.CharField(max_length=200, help_text="divisions")

    publication_date = forms.DateField( required=False )
    online_date = forms.DateField( required=False )
    accept_date = forms.DateField(required=False )
    submit_date = forms.DateField(required=False )
    complete_date = forms.DateField(required=False )

    keywords = forms.CharField(max_length=200, help_text="", required=False, widget=forms.Textarea())
    notes = forms.CharField(max_length=200, help_text="", required=False, widget=forms.Textarea())
    suggestions = forms.CharField(max_length=200, help_text="", required=False, widget=forms.Textarea())
    book_series = forms.CharField(max_length=200, help_text="", required=False, widget=forms.TextInput(attrs={'size': 40}))
    journal = forms.CharField(max_length=200, help_text="", required=False, widget=forms.TextInput(attrs={'size': 40}) )
    volume = forms.CharField(max_length=200, help_text="", required=False)
    issue = forms.CharField(max_length=200, help_text="", required=False)
    publisher = forms.CharField(max_length=200, help_text="", required=False, widget=forms.TextInput(attrs={'size': 40}))
    place_of_pub = forms.CharField(max_length=200, help_text="", required=False)
    pagerange = forms.CharField(max_length=200, help_text="", required=False)
    pages = forms.CharField(max_length=200, help_text="", required=False)
    issn_e = forms.CharField(max_length=200, help_text="", required=False)
    issn_p = forms.CharField(max_length=200, help_text="", required=False)
    issn_l = forms.CharField(max_length=200, help_text="", required=False)
    isbn = forms.CharField(max_length=200, help_text="", required=False)
    book_title = forms.CharField(max_length=200, help_text="", required=False, widget=forms.TextInput(attrs={'size': 40}))
    doi = forms.CharField(max_length=200, help_text="", required=False)
    pubmedid = forms.CharField(max_length=200, help_text="", required=False)
    wosid = forms.CharField(max_length=200, help_text="", required=False)

    status = forms.CharField(widget=forms.HiddenInput(), initial='I')
    publication_status = forms.CharField(widget=forms.HiddenInput(), initial='U')
    visibility_status = forms.CharField(widget=forms.HiddenInput(), initial='N')
    revision = forms.IntegerField(widget=forms.HiddenInput(), initial='1')

    class Meta:
        model = Publication
        fields = ('depositor', 'publication_type', 'title', 'abstract', 'subject', 'divisions', 
                'publication_date', 'online_date', 'accept_date', 'submit_date', 'complete_date', 
                'keywords', 'notes', 'suggestions', 'book_series', 'journal', 'volume', 'issue', 
                'publisher', 'place_of_pub', 'pagerange', 'pages', 'issn_e', 'issn_p', 'issn_l', 
                'isbn', 'book_title', 'doi', 'pubmedid', 'wosid', 'status', 'publication_status', 
                'visibility_status' )


class PublicationFormAddDoc(forms.ModelForm):

    doc_type = forms.CharField(
        max_length=3,
        widget=forms.Select(choices=DOCUMENT_TYPES),
        help_text="Please enter the Document Type")
 
    visibility_status = forms.CharField(
        max_length=1,
        widget=forms.Select(choices=VISIBILITY_STATES),
        help_text="Please enter the Document Type")

    embargo = forms.DateField(help_text="Embargo", 
        widget=forms.DateInput(),
        required=False)

    licence = forms.CharField(
        max_length=5,
        widget=forms.Select(choices=LICENCES),
        help_text="Please enter the Document Type")

    description = forms.CharField(help_text="Description", 
        widget=forms.Textarea(),
        required=False)
    
    filefield = forms.FileField(widget=forms.ClearableFileInput(), required=False )

    class Meta:
        model = Document
        fields = ('doc_type', 'visibility_status', 'embargo', 'licence', 'description', 'filefield')


