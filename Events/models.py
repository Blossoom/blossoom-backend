from operator import attrgetter
from django.db import models
from django.contrib.auth.models import User
from utils.models import BasicTimesince

# Create your models here.

class Event(models.Model, BasicTimesince):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(max_length=1024, blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=250, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    attendees = models.ManyToManyField(User, blank=True, related_name='event_attend')

    
    def total_attendees(self):
        """ Return total number of attendees
        """
        return self.attendees.count()

    def humanized_date(self):
        from django.contrib.humanize.templatetags import humanize
        return humanize.naturalday(self.date)

    def __str__(self) -> str:
        return f"{self.title} {self.humanized_date()}"
