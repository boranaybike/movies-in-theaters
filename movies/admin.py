from django.contrib import admin
from .models import Movie



class MovieAdmin(admin.ModelAdmin):
    list_display= ('id', 'name', 'release_date', 'playing_now')
    list_display_links = ('id', 'name')
    list_filter = ('release_date',)
    list_editable = ('playing_now',)
    search_fields = ('name', 'description')
    list_per_page = 10
# Register your models here.

admin.site.register(Movie, MovieAdmin)