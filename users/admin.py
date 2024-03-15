from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserCredential
from .models import UserEvent, UserSubscription, User


@admin.register(UserCredential)
class UserCredentialAdmin(admin.ModelAdmin):
    list_display = ("client_id", "user")
    search_fields = ("user", "client_id")
    readonly_fields = ("credentials",)


@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    list_display = ("eid", "user", "event")
    search_fields = ("eid", "user__username", "event__name")


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("team", "user")
    search_fields = ("team__popular_name", "user__username")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # fieldsets = BaseUserAdmin.fieldsets + (("Additional Info", {"fields": ("events", "subscriptions")}),)
    # filter_horizontal = (
    #     "events",
    #     "subscriptions",
    # )
    ...
