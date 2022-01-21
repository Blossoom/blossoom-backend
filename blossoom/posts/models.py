from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from votes.models import Vote


# Create your models here.

def upload_to(instance, filename):
    return "posts/{}".format(filename)


class Base(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(max_length=1024, blank=True)
    mediafile = models.FileField(upload_to=upload_to,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    votes = GenericRelation(Vote)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return "{}: {}".format(self.title, self.content[:10])


class Artwork(Base):
    tags = models.ManyToManyField('tags.Tag', related_name='artwork_tags', blank=True)


class Question(Base):
    pass