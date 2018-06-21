from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page

def index(request):
    context = RequestContext(request)
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {"categories": category_list}
    return render_to_response('rango/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)
    data = {"linkname" : "Go back to Home page"}
    return render_to_response("rango/about.html", data, context)

def show_category(request, categoryname):
    context_dict = {}
    context = RequestContext(request)
    try:
        category = Category.objects.get(slug=categoryname)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render_to_response('rango/category.html', context_dict, context)
    
