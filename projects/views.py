from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Projects index")

def detail(request, proj_id):
    return HttpResponse("Project: %s" % proj_id)

