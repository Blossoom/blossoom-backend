from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.


class Notification(models.Model):

    class NotificationTypes(models.TextChoices):
        LIKE = ('lk', 'like')
        COMMENT = ('cm', 'comment')
        FOLLOW = ('fl', 'follow')

    # Backend information
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id= models.PositiveIntegerField()

    # user information
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    trigger = GenericForeignKey('content_type', 'object_id')
    notification_type = models.CharField(max_length=2, choices=NotificationTypes.choices)


    def __str__(self) -> str:
        return f"FROM {self.sender.profile} ON {self.trigger}"
