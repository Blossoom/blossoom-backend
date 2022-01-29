from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from utils.functions import get_model_from_any_app

from comments import serializers

from .models import Comment
from .serializers import CommentSerializer


class CommentViewset(viewsets.ModelViewSet):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    def get_queryset(self):
        post = self.custom_get_object()
        return post.comments.all().order_by('-created') if post else super().get_queryset()

    def custom_get_object(self):
        """ Dynamically get model based on the url lookup name 
        """
        model = self.get_correct_model()
        model = model if model else None
        return get_object_or_404(model, pk=self.kwargs[next(iter(self.kwargs))]) if model else None

    def get_correct_model(self):
        """ Dynamically get model from name.
        """
        return get_model_from_any_app(list(self.kwargs.keys())[0].split('_')[0]) if self.kwargs.keys() else None
    

    def perform_create(self, serializer):
        """ Overwrite perform_create to auto assign contenttype, user object_id
        """
        obj = self.custom_get_object()
        serializer.save(
            user = self.request.user,
            content_type = ContentType.objects.get_for_model(obj),
            object_id = obj.id
        )
