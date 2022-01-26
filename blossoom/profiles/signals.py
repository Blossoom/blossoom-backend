from django.contrib.auth.models import User
from django.db.models.signals import post_save

from .models import Profile


def create_profile(sender, instance, created, **kwargs):
    """
    Automatically create a user profile.
    """

    if created:
        Profile.objects.create(user=instance, username=instance.username)

def save_profile(sender, instance, **kwargs):
    """
    Automatically create a user profile.
    """

    instance.profile.save()


post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=User)
