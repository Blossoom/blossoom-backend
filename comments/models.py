from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from utils.models import BasicTimesince


class Comment(models.Model, BasicTimesince):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id= models.PositiveIntegerField()
    post = GenericForeignKey('content_type', 'object_id')

    content = models.TextField(max_length=1000)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    votes = GenericRelation('votes.Vote')
    
    # to delete notification when comment is deleted
    notifications = GenericRelation('notifications.Notification')

    def __str__(self):
        return f"[{self.created}] | {self.user} {self.content[:20]}"
