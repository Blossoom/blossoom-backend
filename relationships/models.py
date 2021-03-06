from django.db import models
from profiles.models import Profile
from django.contrib.contenttypes.fields import GenericRelation


# Create your models here.
class Relationship(models.Model):

    follow_from = models.ForeignKey(Profile, related_name="following", on_delete=models.CASCADE)
    follow_to = models.ForeignKey(Profile, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    notifications = GenericRelation('notifications.Notification')

    class Meta:
       unique_together = ("follow_from", "follow_to")


    def __str__(self) -> str:
        return f"Follow action TO {self.follow_to}"
