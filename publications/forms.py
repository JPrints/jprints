from django import forms

from .models import Milestone, Contributor, Publication, PUBLICATION_TYPES
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

