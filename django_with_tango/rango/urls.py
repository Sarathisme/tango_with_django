from django.urls import path, re_path, include
from rango import views

urlpatterns = [
    path('',views.index),
    path('about/', views.about),
    path('category/<categoryname>', views.show_category)
]