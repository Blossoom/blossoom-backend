from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from utils.models import BasicTimesince

# Create your models here.


class Notification(models.Model, BasicTimesince):

    class NotificationTypes(models.TextChoices):
        UPVOTE = ('upvote', 'like')
        DOWNVOTE = ('downvote', 'like')
        COMMENT = ('comment', 'comment')
        FOLLOW = ('follow', 'follow')

    # Backend information
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    
    # Generic relation required fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id= models.PositiveIntegerField()
    trigger = GenericForeignKey('content_type', 'object_id')

    # user information
    seen = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=10, choices=NotificationTypes.choices)


    def __str__(self) -> str:
        return f"FROM {self.sender.profile} ON {self.trigger}"
