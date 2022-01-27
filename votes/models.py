from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class Vote(models.Model):
    
    CHOICES = (
        ('upvote', 'upvote'),
        ('downvote', 'downvote'),
        )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=20, choices=CHOICES)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id= models.PositiveIntegerField()
    post = GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField(auto_now_add=True)
    notifications = GenericRelation('notifications.Notification')



    def __str__(self):
        return f"[{self.created}] | {self.user} {self.value} {self.post}"
