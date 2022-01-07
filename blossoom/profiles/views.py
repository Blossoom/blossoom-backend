from django.shortcuts import render
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer, RelationsSerializer


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
    
    def list(self, request):
        """
        Overwrite viewset method.
        """
        raise MethodNotAllowed(request.method)

    @action(methods=['get'], detail=True)
    def followers(self, request, pk):
        """
        Returns object followers
        """
        profile = get_object_or_404(Profile, pk=pk)
        data = RelationsSerializer(
            [relation.follow_from for relation in profile.followers.all()],
            many=True, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def followings(self, request, pk):
        """
        Returns object followers
        """
        profile = get_object_or_404(Profile, pk=pk)
        data = RelationsSerializer(
            [relation.follow_to for relation in profile.following.all()],
            many=True, context={'request': request}).data
        return Response(data, status=status.HTTP_200_OK)


