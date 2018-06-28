from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from rango.models import Category, Page, User, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.webhoseio_search import get_results

def index(request):
    print("Here at index")
    visitor_cookie_handler(request)
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    print(request.session.get('visits')) 
    context_dict = {"categories": category_list, 'visits': request.session.get('visits'), 'pages': pages_list}
    response = render(request, 'rango/index.html', context_dict)
    print("COOKIE VISITS ", request.session['visits'])
    return response

def about(request):
    data = {"linkname" : "Go back to Home page", 'visits': request.session.get(request.user.username)}
    return render(request, "rango/about.html", data)

def show_category(request, category_name):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST.get('query').strip()

        if query:
            result_list = get_results(query)
            context_dict['result_list'] = result_list
            context_dict['query'] = query
        
    try:
        category = Category.objects.get(slug=category_name)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    
    if not context_dict['query']:
        context_dict['query'] = category.name

    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)

        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form':form})

@login_required
def add_page(request, category_name_slug):
    form = PageForm()
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.pictures = request.FILES['picture']

            profile.save()

            registered=True
        else:
            print(user_form.errors, profile_form.errors)
    else:

        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form':profile_form, 'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                user_cookie_handler(request, username)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account is disabled!')
        else:
            print("Invalid login details", username, password)
            return HttpResponse("Invalid details")
    else:
        return render(request, 'rango/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if(datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

def user_cookie_handler(request, name):
    visits = int(get_server_side_cookie(request, name, '1'))
    request.session[name] = visits

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        return default_val
    else:
        return val

def search(request):
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = get_results(query)
    
    return render(request,'rango/search.html', {'result_list': result_list})

def track_url(request):
    if request.method == 'GET':
        if 'pageid' in request.GET:
            page = Page.objects.get(id=request.GET['pageid'])
            page.views = page.views + 1
            page.save()
    else:
        return HttpResponseRedirect(reverse(index))
    
    return redirect(page.url)

@login_required
def like_category(request):
    cat_id = None        
    if request.method == 'GET':
        cat_id = request.GET.get('category_id')
        likes = 0

    if cat_id:
        cat = Category.objects.get(id = int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()

    return HttpResponse(likes)

def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET.get('suggestion')
        flag = request.GET.get('flag')
    cat_list = get_category_list(8, starts_with, flag)
    return render(request, 'rango/cats.html', {'cats': cat_list})

def get_category_list(max_results=0, starts_with='', flag=False):
    cat_list = []
    if flag:
        if starts_with:
            cat_list = Category.objects.filter(name__istartswith=starts_with)
        else:
            cat_list = Category.objects.all()

    if max_results > 0 and flag:
        if len(cat_list) > max_results:
            cat_list = cat_list[0: max_results]
    return cat_list

@login_required
def insert_page(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        url = request.GET.get('url')
        category = request.GET.get('category')

        if category:
            category = Category.objects.get(slug=category)
            page = Page.objects.get_or_create(category=category, title=title, url=url)[0]
            page.save()
        else:
            return HttpResponse('Failure')
        
        return HttpResponse('Success')

@login_required
def profile(request):
    cat_list = get_category_list()
    context_dict = {'cat_list': cat_list}
    u = User.objects.get(username=request.user)
    
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None
    
    context_dict['user'] = u
    context_dict['userprofile'] = up
    return render(request, 'rango/profile.html', context_dict)
