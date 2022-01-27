"""
Notification signals from other models
"""

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification


@receiver(post_save, sender='relationships.Relationship')
def new_follower_signal(sender, instance, **kwargs):
    """
    Create a notification for new follower
    """

    Notification.objects.create(
        sender = instance.follow_from.user,
        recipient = instance.follow_to.user,
        content_type = ContentType.objects.get_for_model(sender),
        object_id = instance.id,
        notification_type="follow"
    ).save()


@receiver([post_save], sender='votes.Vote')
def upvote_downvote_signal(sender, instance, **kwargs):
    """
    Create a notification for upvotes/downvotes
    """

    Notification.objects.create(
            sender = instance.user,
            recipient = instance.post.user,
            content_type = ContentType.objects.get_for_model(sender),
            object_id = instance.id,
            notification_type=instance.value
        ).save()


@receiver([post_save], sender='comments.Comment')
def comment_signal(sender, instance, **kwargs):
    """
    Create a notification for comments
    """

    Notification.objects.create(
            sender = instance.user,
            recipient = instance.post.user,
            content_type = ContentType.objects.get_for_model(sender),
            object_id = instance.id,
            notification_type="comment"
        ).save()
