import os 
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_with_tango.settings')
django.setup()

from rango.models import Category, Page


def populate():
# First, we will create lists of dictionaries containing the pages
# we want to add into each category.
# Then we will create a dictionary of dictionaries for our categories_values. # This might seem a little bit confusing, but it allows us to iterate # through each data structure, and add the data to our models.

    python_pages = [
        {"title": "Official Python Tutorial",
         "url":"http://docs.python.org/2/tutorial/"},
        {"title":"How to Think like a Computer Scientist",
         "url":"http://www.greenteapress.com/thinkpython/"},
        {"title":"Learn Python in 10 Minutes",
         "url":"http://www.korokithakis.net/tutorials/python/"}
    ]

    django_pages = [
        {"title":"Official Django Tutorial",
         "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title":"Django Rocks",
         "url":"http://www.djangorocks.com/"},
        {"title":"How to Tango with Django",
         "url":"http://www.tangowithdjango.com/"} 
    ]

    other_pages = [
        {"title":"Bottle",
         "url":"http://bottlepy.org/docs/dev/"},
        {"title":"Flask",
         "url":"http://flask.pocoo.org"} ]

    cats = {
        "Python": {"pages": python_pages},
        "Django": {"pages": django_pages},
        "Other Frameworks": {"pages": other_pages} 
    }

    categories_values = {
        "Python": {
            "views": 128,
            "likes": 64,
        },
        "Django": {
            "views": 64,
            "likes": 32,
        },
        "Other Frameworks": {
            "views": 32,
            "likes": 16,
        }
    }

    for cat, cat_data in cats.items(): 
        c = add_cat(cat, categories_values[cat]['views'], categories_values[cat]['likes'])
        for p in cat_data["pages"]:
                add_page(c, p["title"], p["url"])
    # Print out the categories_values we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0] 
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0] 
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...") 
    populate()