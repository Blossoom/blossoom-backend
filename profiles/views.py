from django import http
from django.db.models import Q
from django.shortcuts import get_object_or_404
from jinja2 import pass_context
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from posts.models import Artwork, Question

from .models import Profile
from .serializers import BasicUserDisplaySerializer, ProfileSerializer

# Create your views here.


class ProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    A viewset for editing and viewing profiles
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        query = self.request.query_params.get('user') or ''
        users = Profile.objects.filter(
            Q(name__icontains=query)  | 
            Q(username__icontains=query)   |
            Q(bio__icontains=query) 
        ).order_by('-followers')
        return users

    def perform_update(self, serializer):

        if self.request.user.profile.is_new:
            serializer.save(is_new=False)
        else:
            serializer.save()

    @action(methods=['get'], detail=True)
    def followers(self, request, pk=None):
        """
        Returns object followers
        """
        profile = get_object_or_404(Profile, pk=pk)
        data = BasicUserDisplaySerializer(
            [relation.follow_from for relation in profile.followers.all()],
            many=True, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def followings(self, request, pk=None):
        """
        Returns object followers
        """
        profile = get_object_or_404(Profile, pk=pk)
        data = BasicUserDisplaySerializer(
            [relation.follow_to for relation in profile.following.all()],
            many=True, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def follow(self, request, pk=None):
        """
        Follow and unfollow profile.
        """

        from relationships.models import Relationship

        current_user_profile = request.user.profile if not request.user.is_anonymous else None
        if not current_user_profile:
            return Response({ "detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)


        target_profile = get_object_or_404(Profile, pk=pk)


        if target_profile == current_user_profile:
            return Response({"detail": "User cant follow his profile."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        relation = current_user_profile.following.filter(follow_to=target_profile)
        if relation.exists():
            relation.delete()
            return Response({"detail": "Unfollow success."}, status=status.HTTP_200_OK)
        else:
            Relationship.objects.create(
                follow_from = current_user_profile,
                follow_to = target_profile
            )
            return Response({"detail": "Follow success."}, status=status.HTTP_200_OK)
    

    @action(methods=['get'], detail=True)
    def saved(self, request, pk=None):
        """ Get user saved posts
        """
        from posts.serializers import GeneralPostSerializer
        from articles.serializers import ArticleSerializer

        if request.user.is_anonymous or request.user.profile.pk != pk:
            return Response({ "detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        artworkSerializer = GeneralPostSerializer
        questionSerializer = GeneralPostSerializer 

        artworkSerializer.Meta.model = Artwork
        questionSerializer.Meta.model = Question

        article_post = request.user.article_save.all()
        artwork_post = request.user.artwork_save.all()
        question_post = request.user.question_save.all()

        data = {
            'articles' :  ArticleSerializer(article_post, many=True, context={'request': request}).data,
            'artworks' :  GeneralPostSerializer(artwork_post, many=True, context={'request': request}).data,
            'questions': GeneralPostSerializer(question_post, many=True, context={'request': request}).data
        }
        return Response(data, status=status.HTTP_200_OK)






