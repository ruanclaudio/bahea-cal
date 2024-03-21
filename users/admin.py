from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserCredential
from .models import UserEvent, UserSubscription, User


@admin.register(UserCredential)
class UserCredentialAdmin(admin.ModelAdmin):
    list_display = ("client_id", "user", "created", "modified")
    search_fields = ("user", "client_id")
    readonly_fields = ("credentials",)


@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    list_display = ("eid", "user", "event", "created", "modified")
    search_fields = ("eid", "user__username", "event__name")


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("team", "user", "created", "modified")
    search_fields = ("team__popular_name", "user__username")


class UserEventsAdmin(admin.TabularInline):
    model = User.events.through


class UserSubscriptionsAdmin(admin.TabularInline):
    model = User.subscriptions.through


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (("Additional Info", {"fields": ("calendar_id",)}),)
    inlines = (UserEventsAdmin, UserSubscriptionsAdmin)
