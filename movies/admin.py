from django.contrib import admin
from .models import Movie, Review, MovieRequest

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class MovieRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'requested_by', 'date_requested']
    list_filter = ['date_requested']
    search_fields = ['title', 'requested_by__username']
    ordering = ['-date_requested']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(MovieRequest, MovieRequestAdmin)