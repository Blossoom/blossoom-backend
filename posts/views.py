from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from utils.functions import get_model_from_any_app

from .models import Artwork, Question
from .serializers import GeneralPostSerializer

# Create your views here.


class ArtworkViewset(ModelViewSet):

    queryset = Artwork.objects.all()
    serializer_class = GeneralPostSerializer

    def get_serializer_class(self):
        self.serializer_class.Meta.model=get_model_from_any_app(
            self.get_parser_context(self.request).get('view').basename)
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        query = self.request.query_params.get('q') or ''
        query = query if query in ['hot', 'relevant', 'latest'] else ''

        # TODO: This part need to be redesigned
        
        posts = super().get_queryset()
        
        # get posts related to user
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


class QuestionViewset(ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = GeneralPostSerializer


    def get_serializer_class(self):
        self.serializer_class.Meta.model=get_model_from_any_app(
            self.get_parser_context(self.request).get('view').basename)
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def get_queryset(self):
        query = self.request.query_params.get('q') or ''
        query = query if query in ['hot', 'relevant', 'latest'] else ''

        # TODO: This part need to be redesigned

        # get posts related to user
        posts = super().get_queryset().order_by('-created')

        if not self.request.user.is_anonymous:

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
