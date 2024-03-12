from django.contrib import admin
from .models import UserCredential


@admin.register(UserCredential)
class UserCredentialAdmin(admin.ModelAdmin):
    list_display = ("client_id", "user")
    search_fields = ("user", "client_id")
    readonly_fields = ("credentials",)
