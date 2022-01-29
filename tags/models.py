from pydoc import describe
from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=150, null=False, blank=False)
    description = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name