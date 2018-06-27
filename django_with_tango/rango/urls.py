from django.urls import path, re_path, include
from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^about/$', views.about, name="about"),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^like_category/$', views.like_category, name='like_category'),
    url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
    url(r'^insert_page/$', views.insert_page, name='insert_page'),
    url(r'^profile/$', views.profile, name='profile'),
]