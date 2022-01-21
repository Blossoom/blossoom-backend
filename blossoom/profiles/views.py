from inspect import currentframe
from itertools import permutations
from django.shortcuts import render
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer, BasicUserDisplaySerializer


# Create your views here.


class ProfileViewSet(ModelViewSet):
    """
    A viewset for editing and viewing profiles
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


    def create(self, request, *args, **kwargs):
        """
        Overwrite viewset method.
        """
        raise MethodNotAllowed(request.method)

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






