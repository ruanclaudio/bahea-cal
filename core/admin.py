from django.contrib import admin
from .models import Team, Championship, Location, Phase, Round, Match, SoccerEvent


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("popular_name", "created", "modified")
    search_fields = ("popular_name",)


@admin.register(Championship)
class ChampionshipAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "modified")
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "popular_name", "created", "modified")
    search_fields = ("name", "popular_name")


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ("name", "phase_type", "created", "modified")
    search_fields = ("name", "phase_type")


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "modified")
    search_fields = ("name",)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "championship",
        "home_team",
        "away_team",
        "location",
        "phase",
        "round",
        "start_at",
        "created",
        "modified",
    )
    search_fields = (
        "championship__name",
        "home_team__popular_name",
        "away_team__popular_name",
        "location__popular_name",
        "phase__name",
        "round__name",
    )
    list_filter = ("championship", "home_team", "away_team", "location", "phase", "round")


@admin.register(SoccerEvent)
class SoccerEventAdmin(admin.ModelAdmin):
    list_display = ("match", "created", "modified")
    search_fields = ("match__id",)
