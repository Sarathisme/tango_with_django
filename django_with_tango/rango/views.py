from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    context = RequestContext(request)
    context_dict = {"boldmessage": "This is a template message"}
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)
    data = {"linkname" : "Go back to Home page"}
    return render_to_response("rango/about.html", data, context)
