from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile_pic','user_id')
    list_display_links = ('id', 'user')
    list_per_page = 10

admin.site.register(Profile,ProfileAdmin)