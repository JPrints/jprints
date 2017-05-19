from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from core.models import Person, Role, Permission
from .models import Publication, Document, Contributor

#from publications.forms import PublicationFormAdmin
from publications.forms import PublicationForm, PublicationFormAddDoc

import logging
import re


def index(request):
    latest_pubs = Publication.objects.order_by('-lastmod')[:5]
    context = { 'latest_publication_list': latest_pubs, }
    return render(request, 'publications/index.html', context)

def detail(request, pk):
    publication = get_object_or_404(Publication, id=pk)
    documents = Document.objects.filter(publication__id=pk)
    print("\n\n\n############# Detail ################");
    contributors = Contributor.objects.filter(publication=publication).order_by('number');
    print("contributors", contributors);

    context = { 'publication': publication, 'publication_id': pk, 'documents': documents, 'contributors':contributors }
    return render(request, 'publications/detail.html', context)

@login_required
def add_publication(request):

    logger = logging.getLogger('jprints')
    person = request.user.person
    form = PublicationForm()

    if (person.user_type == "Ad"):
        #form = PublicationForm()
        logger.info("Person is admin")
    else:
        #form = PublicationFormAdmin(request.POST)
        #form = PublicationForm()
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
    from random import randint
    from django.contrib.auth.models import User
    from core.models import Person, Role, Permission
    from .models import Contributor

    if request.method == 'POST':
        print("##############edit_publication called, POST param is", pubid) 
        pub_orig = Publication.objects.get(pk=pubid)
        pub_form = PublicationForm(data=request.POST, instance=pub_orig)

        if pub_form.is_valid():
            pub = pub_form.save()
            # get any new contributors
            contrib_count = request.POST.get("contrib_count", 0)
            contribs = {}
            req_items = request.POST.items();
            # create a dict for each position

            for req_item in req_items:
                m = re.match( r"contrib_entry_(\w+)_(\d+)" , req_item[0] )
                if m and m.group(1) and m.group(2):
                    if m.group(2) not in contribs:
                        contribs[ m.group(2) ] = {};
                    contribs[ m.group(2) ][m.group(1)] = req_item[1];
            #delete existing contributors
            Contributor.objects.filter(publication=pub).delete();

            for id, contrib in contribs.items():
                print( id, contrib )
                person = None
                try:
                    person = Person.objects.get(pk=contrib['i'])
                except ObjectDoesNotExist:
                    username = contrib['f']+str(randint(1,10000))
                    print("USERNAME", username);
                    u = User.objects.get_or_create(username=username, email="", first_name=contrib['g'], last_name=contrib['f'])[0]
                    u.save()
                    person = Person.objects.get_or_create(user=u)[0]
                    person.disp_title = contrib['t']
                    person.disp_given = contrib['g']
                    person.disp_family = contrib['f']
                    person.lang = "EN"
                    person.orcid = contrib['o']
                    person.user_type = 'Ex'
                    person.save()
 
                    print("PERSON DOES NOT EXIST", contrib['i']);
                if person is None:
                    print("NO PERSON FOUND for ", contrib['i'] )
                contrib_type = 'Au'
                contributor = Contributor(person=person, contribution_type = contrib_type, number = contrib['p'], publication=pub )
                contributor.save()

            #if 'photo' in request.FILES:
            #    person.photo = request.FILES['photo']
            pub.save()
            return detail(request, pubid)
        else:
            print(pub_form.errors)
            context = { 'pub': pub_orig, 'pub_form': pub_form }
            return render(request, 'publications/edit.html', context)

    else: 
        print("##############edit_publication called, GET param is", pubid) 
        pub = Publication.objects.get(pk=pubid)
        contributors = Contributor.objects.filter(publication=pub).order_by('number');
        form = PublicationForm(instance=pub)
        context = { 'pub': pub, 'contributors': contributors, 'pub_form': form }
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

@login_required
def add_contributor(request, personid):

    logger = logging.getLogger('jprints')
    logger.info("add_contributor called ")

    if request.method == 'POST':
        #person = Publication.objects.get(pk=personid)
        logger.info("request is POST")
        #print("add_doc pub is", pub) 

        #doc_form = PublicationFormAddDoc(data=request.POST)

        #doc_is_valid = doc_form.is_valid()
        #print("doc is valid ["+str(doc_is_valid)+"]")
        #if doc_form.is_valid():
        #    doc = doc_form.save(commit=False)
        #    doc.publication = pub
        #    doc.save()

        #    print("GOT DOCUMENT!!!!! "+str(request.FILES))
        #    if 'filefield' in request.FILES:
        #        print("GOT DOCUMENT!!!!! "+str(request.FILES))
        #        doc.filefield = request.FILES['filefield']
        #    doc.save()
        #    return detail(request, personid)
        #else:
        #    print(doc_form.errors)
        #    context = { 'pub': pub, 'doc_form': doc_form }
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




