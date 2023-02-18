from django.contrib import admin

from app_users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'phone']
    list_display_links = ['user']
    search_fields = ['city', 'phone']
