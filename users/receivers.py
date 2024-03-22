import arrow
from django.apps import apps
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserSubscription


@receiver(post_save, sender=UserSubscription)
def update_user_events(sender, instance, created, **kwargs):
    now = arrow.utcnow()

    event_model = apps.get_model("core", "SoccerEvent")

    for event in event_model.objects.filter(match__start_at__gte=now.datetime).filter(
        Q(match__home_team=instance.team) | Q(match__away_team=instance.team)
    ):
        instance.user.events.add(event)
