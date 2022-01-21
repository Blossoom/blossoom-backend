from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


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

    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"[{self.timestamp}] | {self.user} {self.value} {self.post}"