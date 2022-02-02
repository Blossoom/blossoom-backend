from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q


class CustomPostModelViewset(viewsets.ModelViewSet):

    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        """ Overwrite queryset for posts that contain tags
        """
        query = self.request.query_params.get('q') or ''
        query = query if query in ['hot', 'relevant', 'latest'] else ''

        # TODO: This part need to be redesigned        
        posts = super().get_queryset()
        
        # get posts related to user
        if not self.request.user.is_anonymous:
            posts.filter(Q(tags__in=self.request.user.profile.tags.all())
            ).order_by('-created')

            if query == 'relevant':
                posts = posts.filter(Q(
                    user__profile__in=[
                        relationship.follow_to.id for relationship
                        in self.request.user.profile.following.all()
                    ])).order_by('-created')
            
        if query == 'hot':
            posts = posts.order_by('-votes', '-created')

        return posts

    @action(methods=['get'], detail=False, url_path='users/(?P<user_pk>[^/.]+)')
    def users(self, request, user_pk=None):
        """ Get logged in user posts 
        """
        myposts = self.queryset.filter(user__profile__id=user_pk)
        serializer = self.get_serializer(myposts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def save(self, request, pk=None):
        """ User can save posts.
        """
        if request.user.is_anonymous:
            return Response({ "detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        post = get_object_or_404(self.queryset.model, pk=pk)

        if request.user in post.saves.all():
            post.saves.remove(request.user)
            return Response({'detail': 'post unsaved'}, status=status.HTTP_200_OK)
        
        post.saves.add(self.request.user)
        return Response({'detail': 'post saved'}, status=status.HTTP_200_OK)