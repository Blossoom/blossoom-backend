"""
Notification signals from other models
"""

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from .models import Notification


def new_follower_signal(sender, instance, **kwargs):
    """
    Create a notification for neww follower
    """

    Notification.objects.create(
        sender = instance.follow_from.user,
        recipient = instance.follow_to.user,
        content_type = ContentType.objects.get_for_model(sender),
        object_id = instance.id,
        notification_type="fl"
    ).save()

post_save.connect(new_follower_signal, sender='relationships.Relationship')


