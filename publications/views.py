from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Publication, Document
#from publications.forms import PublicationFormAdmin
from publications.forms import PublicationFormAdmin, PublicationFormDepositor, PublicationFormAddDoc

import logging


def index(request):
    latest_pubs = Publication.objects.order_by('-lastmod')[:5]
    context = { 'latest_publication_list': latest_pubs, }
    return render(request, 'publications/index.html', context)

def detail(request, pk):
    publication = get_object_or_404(Publication, id=pk)
    documents = Document.objects.filter(publication__id=pk)
    context = { 'publication': publication, 'publication_id': pk, 'documents': documents }
    return render(request, 'publications/detail.html', context)

@login_required
def add_publication(request):

    logger = logging.getLogger('jprints')
    person = request.user.person
    form = PublicationFormDepositor( person )

    if (person.user_type == "Ad"):
        form = PublicationFormAdmin()
        logger.info("Person is admin")
    else:
        #form = PublicationFormAdmin(request.POST)
        form = PublicationFormDepositor( person )
        logger.info("Person is NOT admin")

    if request.method == 'POST':
        logger.info("request is POST")
        if form.is_valid():
            new_pub = form.save(commit=True)
            return detail(request, new_pub.id)
        else:
            print(form.errors)
    else:
        logger.info(__name__+": request is NOT POST")

#        if (person.user_type == "Ad"):
#            form = PublicationFormAdmin( person )
#            form.fields['depositor'].initial = person.id
#        else:
#            form = PublicationFormDepositor( person )

    return render(request, 'publications/add_publication.html', {'form': form})


@login_required
def edit_publication(request, pubid):

    if request.method == 'POST':
        print("edit_profile called, POST param is", pubid) 
        pub_orig = Publication.objects.get(pk=pubid)
        print("edit_publication pub is", pub_orig) 

        pub_form = PublicationFormAdmin(data=request.POST, instance=pub_orig)

        if pub_form.is_valid():
            pub = pub_form.save()
            #if 'photo' in request.FILES:
            #    person.photo = request.FILES['photo']
            pub.save()
            return detail(request, pubid)
        else:
            print(pub_form.errors)
            context = { 'pub': pub, 'pub_form': pub_form }
            return render(request, 'publications/edit.html', context)

    else: 
        print("edit_profile called, GET param is", pubid) 
        pub = Publication.objects.get(pk=pubid)
        form = PublicationFormAdmin(instance=pub)
        context = { 'pub': pub, 'pub_form': form }
        return render(request, 'publications/edit.html', context)

@login_required
def add_doc(request, pubid):

    logger = logging.getLogger('jprints')
    logger.info("add_doc called ")

    if request.method == 'POST':
        pub = Publication.objects.get(pk=pubid)
        logger.info("request is POST")
        print("add_doc pub is", pub) 

        doc_form = PublicationFormAddDoc(data=request.POST)

        doc_is_valid = doc_form.is_valid()
        print("doc is valid ["+str(doc_is_valid)+"]")
        if doc_form.is_valid():
            doc = doc_form.save(commit=False)
            doc.publication = pub
            doc.save()

            print("GOT DOCUMENT!!!!! "+str(request.FILES))
            if 'filefield' in request.FILES:
                print("GOT DOCUMENT!!!!! "+str(request.FILES))
                doc.filefield = request.FILES['filefield']
            doc.save()
            return detail(request, pubid)
        else:
            print(doc_form.errors)
            context = { 'pub': pub, 'doc_form': doc_form }
            return render(request, 'publications/add_doc.html', context)

    else: 
        print("add_doc called, GET param is", pubid) 
        pub = Publication.objects.get(pk=pubid)
        form = PublicationFormAddDoc(instance=pub)
        context = { 'pub': pub, 'doc_form': form }
        return render(request, 'publications/add_doc.html', context)



class IndexView(generic.ListView):
    template_name = 'publications/index.html'
    context_object_name = 'latest_publication_list'
    
    def get_queryset(self):
        return Publication.objects.order_by('-lastmod')[:5]




