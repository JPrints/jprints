from django import forms

from .models import Milestone, Contributor, Publication, Document, PUBLICATION_TYPES, DOCUMENT_TYPES, LICENCES, VISIBILITY_STATES
from core.models import Person

class PublicationFormAdmin(forms.ModelForm):

    depositor = forms.ModelChoiceField(queryset=Person.objects.all(), help_text="Depositor", empty_label="Deposit on behalf of")
    publication_type = forms.CharField(
        max_length=1,
        widget=forms.Select(choices=PUBLICATION_TYPES),
        help_text="Please enter the Publication Type")
    title = forms.CharField(max_length=200, help_text="title")
    abstract = forms.CharField(help_text="abstract", 
        widget=forms.Textarea(),
        required=False)
    subject = forms.CharField(max_length=200, help_text="The subjects")
    divisions = forms.CharField(max_length=200, help_text="divisions")

    status = forms.CharField(widget=forms.HiddenInput(), initial='I')
    publication_status = forms.CharField(widget=forms.HiddenInput(), initial='U')
    visibility_status = forms.CharField(widget=forms.HiddenInput(), initial='N')
    revision = forms.IntegerField(widget=forms.HiddenInput(), initial='1')

    class Meta:
        model = Publication
        fields = ('depositor', 'publication_type', 'title', 'abstract', 'subject', 'divisions')

class PublicationFormDepositor(forms.ModelForm):

    def __init__(self, person):
        self.person = person
        print(person)
        super().__init__()

    publication_type = forms.CharField(
        max_length=1,
        widget=forms.Select(choices=PUBLICATION_TYPES),
        help_text="Please enter the Publication Type")
    title = forms.CharField(max_length=200, help_text="title")
    abstract = forms.CharField(help_text="abstract", 
        widget=forms.Textarea(),
        required=False)
    subject = forms.CharField(max_length=200, help_text="The subjects")
    divisions = forms.CharField(max_length=200, help_text="divisions")

    status = forms.CharField(widget=forms.HiddenInput(), initial='I')
    publication_status = forms.CharField(widget=forms.HiddenInput(), initial='U')
    visibility_status = forms.CharField(widget=forms.HiddenInput(), initial='N')
    revision = forms.IntegerField(widget=forms.HiddenInput(), initial='1')

    class Meta:
        model = Publication
        fields = ( 'publication_type', 'title', 'abstract', 'subject', 'divisions')


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


