from re import A
from django.contrib import admin
from .models import Artwork, Question


# Register your models here.
admin.site.register(Artwork)
admin.site.register(Question)