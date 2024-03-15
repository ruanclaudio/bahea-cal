from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SoccerEvent


@receiver(post_save, sender=SoccerEvent)
def update_user_events(sender, instance, created, **kwargs):
    if created:
        home_team_subscriptions = instance.match.home_team.subscriptions.all()
        away_team_subscriptions = instance.match.home_team.subscriptions.all()

        for subscription in home_team_subscriptions:
            subscription.user.events.add(instance)
        for subscription in away_team_subscriptions:
            subscription.user.events.add(instance)
