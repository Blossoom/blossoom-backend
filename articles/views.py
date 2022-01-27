from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer


class ArticleViewset(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        query = self.request.query_params.get('q') or ''
        query = query if query in ['hot', 'relevant', 'latest'] else ''

        # TODO: This part need to be redesigned

        # get posts related to user
        
        posts = super().get_queryset()
        
        if not self.request.user.is_anonymous:
            posts.filter(Q(tags__in=self.request.user.profile.tags.all())
            ).order_by('-created')

            if query == 'relevant':
                posts = posts.filter(Q(user__profile__in=[relationship.follow_to.id for relationship in self.request.user.profile.following.all()])).order_by('-created')
            
        if query == 'hot':
            posts = posts.order_by('-votes', '-created')

        return posts

    @action(methods=['get'], detail=False)
    def me(self, request, pk=None):
        """ Get logged in user posts 
        """
        if request.user.is_anonymous:
            return Response({ "detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        myposts = self.get_queryset().filter(user_id=request.user.id)
        serializer = self.get_serializer(myposts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
