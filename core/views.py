from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import re

from core.forms import UserForm, PersonForm
from core.elastic_search import run_query, run_filter, run_agg_filter
from .models import Person

# Create your views here.

def index(request):
    context = { 'message': "hello", }
    return render(request, 'core/index.html', context)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        person_form = PersonForm(data=request.POST)

        if user_form.is_valid() and person_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            person = person_form.save(commit=False)
            person.user = user
            if 'photo' in request.FILES:
                person.photo = request.FILES['photo']

            person.save()
            registered = True
        else:
            print(user_form.errors)
            print(person_form.errors)

    else:
        # not a POST so render the forms
        user_form = UserForm()
        person_form = PersonForm()

    return render(request,
                    'core/register.html',
                    {'user_form': user_form,
                     'person_form': person_form,
                     'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print( "login request details: {0}, {1}".format(username, password))

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse( "Your account is not active" )
        else:
            print( "Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid Login")
    else:
        return render(request, 'core/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def profile(request):
    context = {}
    if request.user.is_authenticated():
        context = { 'user': request.user }
    return render(request, 'core/profile.html', context)

@login_required
def edit_profile(request, profileid):

    if request.method == 'POST':
        print("edit_profile called, POST param is", profileid) 
        person_orig = Person.objects.get(pk=profileid)
        print("edit_profile person is", person_orig) 

        person_form = PersonForm(data=request.POST, instance=person_orig)

        if person_form.is_valid():
            person = person_form.save()
            if 'photo' in request.FILES:
                person.photo = request.FILES['photo']
            person.save()
            context = { 'user': person.user }
            return render(request, 'core/profile.html', context)
        else:
            print(person_form.errors)
            context = { 'user': person.user, 'person_form': person_form }
            return render(request, 'core/edit.html', context)

    else: 
        person = Person.objects.get(pk=profileid)
        print("edit_profile called, GET param is", profileid) 
        person_form = PersonForm(instance=person)
        context = { 'user': person.user, 'person_form': person_form }
        return render(request, 'core/edit.html', context)


def profiles(request):
    users = User.objects.order_by('last_name')
    context = { 'user_list': users }
    return render(request, 'core/profiles.html', context)


def search(request):
    result_list = []
    print("search")

    if request.method == 'POST':
        query = request.POST['query'].strip()
        print("search query", query)
        if query:
            result_list = run_query(query)
            #print("views.search::result_list: ["+'\n'.join(map(str, result_list))+"]")
    return render(request, 'core/search.html', {'result_list': result_list, 'query': query } )

def filter(request, ftype, ffield ):
    result_list = []
    print("views.filter ["+ftype+"]", ffield)

    result_list = run_filter( ftype, ffield, "B" )
    print("views.filter::result_list: ["+'\n'.join(map(str, result_list))+"]")
    context = { 'result_list': result_list, 
                'type': ftype,    #"Publications", 
                'ffield': ffield 
            }
    return render(request, 'core/filter.html', context )


def browse(request, ftype ):
    result_list = []

    print("BROWSE xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    item_filter_terms = []
    pub_status_filter_terms = []
    status_filter_terms = []
    milestone_terms = []
    filter_terms = []
    query_from = 0
    query_size = 10
    if request.method == 'POST':
        print("BROWSE POST xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        for pr in request.POST.items():
            print("got post item", pr)
            next_btn = re.match( "^next_(?P<from>[0-9]+)_(?P<size>[0-9]+)", pr[0])
            if next_btn:
                print("GOT NEXT BTN", next_btn.group('from'), next_btn.group('size') )
                query_size = int(next_btn.group('size'))
                query_from = int(next_btn.group('from')) + query_size

            prev_btn = re.match( "^prev_(?P<from>[0-9]+)_(?P<size>[0-9]+)", pr[0])
            if prev_btn:
                print("GOT PREV BTN", prev_btn.group('from'), prev_btn.group('size') )
                query_size = int(prev_btn.group('size'))
                query_from = int(prev_btn.group('from')) - query_size
                if query_from < 0:
                    query_from = 0
                print("PREV BTN", query_from, query_size )

            im = re.match( "^item_type_(?P<item>[A-Z]+)", pr[0])
            if im:
                filter_terms.append({"item_type":  im.group('item')})
            pm = re.match( "^pub_status_(?P<item>[A-Z]+)", pr[0])
            if pm:
                filter_terms.append({"pub_status":  pm.group('item')})
            sm = re.match( "^status_(?P<item>[A-Z]+)", pr[0])
            if sm:
                filter_terms.append({"status":  sm.group('item')})
            ym = re.match( "^milestone_(?P<item>[0-9]+)", pr[0])
            if ym:
                the_year =  ym.group('item')+"||/y"
                milestone_terms.append({"milestone":  { "gte": the_year, "lte": the_year, "format": "yyyy" } })

    results = run_agg_filter( ftype, query_from, query_size, filter_terms, milestone_terms )
    result_list = results['hits']
    aggs_list = results['aggs']
    total = results['total']
    qto = query_from + query_size
    if qto > int(total):
        qto = total
    print("from", query_from, "to", qto, "total", total)
    print("views.browse::result_list: ["+'\n'.join(map(str, result_list))+"]")
#    print("views.browse::aggs_list: ["+'\n'.join(map(str, aggs_list))+"]")
    context = { 'result_list': result_list, 
                'aggs_list': aggs_list,
                'btype': ftype, 
                'qfrom': query_from,
                'qto'  : qto,
                'qsize': query_size,
                'total': total,
            }
    return render(request, 'core/browse.html', context )




class DetailView(generic.DetailView):
    model = Person
    template_name = 'core/detail.html'


