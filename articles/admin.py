from django.contrib import admin

from .models import Article, EditorImage

# Register your models here.


admin.site.register(Article)
admin.site.register(EditorImage)