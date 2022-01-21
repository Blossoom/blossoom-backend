from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .models import Vote
from .serializers import VoteSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from utils.functions import get_model_from_any_app



class VoteViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):


    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


    def get(self, request, *args, **kwargs):
        obj =  get_object_or_404(self.get_correct_model(), pk=self.kwargs[next(iter(self.kwargs))])
        return Response(self.get_serializer(obj).data)


    def custom_get_object(self):
        return get_object_or_404(self.get_correct_model(), pk=self.kwargs[next(iter(self.kwargs))])


    def create(self, request, *args, **kwargs):

        # validate data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get post object
        obj = self.custom_get_object()

        # Post obejct generic information
        content_type = ContentType.objects.get_for_model(obj.__class__)
        object_id = getattr(obj, obj.__class__._meta.pk.column)

        print(content_type, object_id)

        # Creating Updating deleting vote
        vote, created = Vote.objects.get_or_create(content_type=content_type, object_id=object_id, user=request.user)

        if vote.value == request.data.get('value'):
            # Removing vote
            vote.delete() 
        else:
            vote.value=request.data['value']
            vote.save()
        
        # Return updated vote data for that post
        data = self.get(request, *args, **kwargs).data 
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


    def get_correct_model(self):
        """ Dynamically get model from kwargs param.
        """
        return get_model_from_any_app(list(self.kwargs.keys())[0].split('_')[0])    