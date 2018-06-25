from django.contrib import admin
from rango.models import Category, Page, UserProfile

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'views', 'likes', 'slug']
    list_display = ('name', 'views', 'likes')
    list_filter = ('name', 'views', 'likes')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

class PageAdmin(admin.ModelAdmin):
    fields = ['category', 'title', 'url', 'views']
    list_display = ('title', 'url', 'views')
    list_filter = ('title', 'views')
    search_fields = ['title']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
