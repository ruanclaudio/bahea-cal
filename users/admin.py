from django.contrib import admin
from .models import UserCredentials


@admin.register(UserCredentials)
class UserCredentialsAdmin(admin.ModelAdmin):
    list_display = ("client_id", "user")
    search_fields = ("user", "client_id")
    readonly_fields = ("credentials",)
