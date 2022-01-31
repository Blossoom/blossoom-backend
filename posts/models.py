from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from utils.models import BasicTimesince

# Create your models here.

def upload_to(instance, filename):
    return "posts/{}".format(filename)


class Base(models.Model, BasicTimesince):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(max_length=1024, blank=True)
    mediafile = models.ImageField(upload_to=upload_to,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    votes = GenericRelation('votes.Vote')
    comments = GenericRelation('comments.Comment')

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return "{}: {}".format(self.title, self.content[:10])


class Artwork(Base):
    tags = models.ManyToManyField('tags.Tag', related_name='artwork_tags', blank=True)


class Question(Base):
    pass
