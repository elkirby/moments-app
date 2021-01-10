from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.context_processors import auth
from django.template import RequestContext


def index(request):
    return render(request, 'index.html', {})
