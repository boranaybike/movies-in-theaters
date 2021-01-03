from django.contrib import admin
from .models import Movie, Comment


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'release_date', 'playing_now')
    list_display_links = ('id', 'name')
    list_filter = ('release_date',)
    list_editable = ('playing_now',)
    search_fields = ('name', 'description')
    list_per_page = 10


admin.site.register(Movie, MovieAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user_id', 'movie_id')
    list_display_links = ('id', 'comment')


admin.site.register(Comment, CommentAdmin)