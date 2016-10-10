from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from core.forms import UserForm, PersonForm

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



