from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import re
import json

from core.models import Person


def lookup_person(request):
    given = request.GET.get('g', default="")
    family = request.GET.get('f', default="")
    orcid = request.GET.get('o', default="")

    person_data = []
    print("lookup_person called", 'given', given, 'family', family, 'orcid', orcid)
    q = Person.objects.all()
    if len(given) > 0:
        q = q.filter(disp_given__icontains=given)
    if len(family) > 0:
        q = q.filter(disp_family__icontains=family)
    if len(orcid) > 0:
        q = q.filter(orcid__icontains=orcid)
    for person in q:
        person_data.append(
            {
                'id': person.id,
                'title': person.disp_title,
                'given': person.disp_given,
                'family': person.disp_family,
                'orcid': person.orcid,
                'email': person.user.email
            }
        )


    print(q)



    #person_data = [
    #    person1,
    #    person2
    #]
    json_data = { 'people': person_data }

    return JsonResponse(json_data)


