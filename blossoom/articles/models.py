from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from utils.models import BasicTimesince

# Create your models here.

def upload_to(instance, filename):
    return "articles/{}".format(filename)


class Article(models.Model, BasicTimesince):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField()
    preview_content = models.TextField(max_length=1024, blank=True)
    preview_image = models.FileField(upload_to=upload_to,blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    comments = GenericRelation('comments.Comment')
    votes = GenericRelation('votes.Vote')
    tags = models.ManyToManyField('tags.Tag', related_name='article_tags', blank=True)

    notifications = GenericRelation('notifications.Notification')


    def __str__(self) -> str:
        return "{}: {}".format(self.title, self.preview_content)
