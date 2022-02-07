from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import mixins

from utils.views import CustomPostModelViewset

from .models import Article
from .serializers import ArticleSerializer, EditorSerializer




class ArticleViewset(CustomPostModelViewset):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class EditorViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = EditorSerializer