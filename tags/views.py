from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Tag
from .serializers import TagSerializer

# Create your views here.


class TagViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer 

    @action(methods=['get'], detail=True)
    def follow(self, request, pk=None):
        """ Follow a tag, if follow exists then it will be removed and vice versa
        """
        
        tag = get_object_or_404(Tag, pk=pk)
        user = request.user.profile if not request.user.is_anonymous else None
        
        if not user:
            return Response({ "detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
            
        if tag in user.tags.all():
            user.tags.remove(tag)
            return Response({"detail": "Tag unfollowed"}, status=status.HTTP_200_OK)

        user.tags.add(tag)
        return Response({"detail": "Tag followed"}, status=status.HTTP_201_CREATED)
