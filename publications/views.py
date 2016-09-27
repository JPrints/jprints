from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Publication
from publications.forms import PublicationForm


def index(request):
    latest_pubs = Publication.objects.order_by('-lastmod')[:5]
    context = { 'latest_publication_list': latest_pubs, }
    return render(request, 'publications/index.html', context)

def mydetail(request, pk):
    publication = get_object_or_404(Publication, id=pk)
    context = { 'publication': publication, 'publication_id': pk }
    return render(request, 'publications/detail.html', context)

@login_required
def add_publication(request):
    form = PublicationForm()

    if request.method == 'POST':
        form = PublicationForm(request.POST)

        if form.is_valid():
            new_pub = form.save(commit=True)
            return mydetail(request, new_pub.id)
        else:
            print(form.errors)

    return render(request, 'publications/add_publication.html', {'form': form})


class IndexView(generic.ListView):
    template_name = 'publications/index.html'
    context_object_name = 'latest_publication_list'
    
    def get_queryset(self):
        return Publication.objects.order_by('-lastmod')[:5]


class DetailView(generic.DetailView):
    model = Publication
    template_name = 'publications/detail.html'




