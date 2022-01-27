from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from utils.functions import get_model_from_any_app

from .models import Vote
from .serializers import VoteSerializer


class VoteViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):


    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = ()


    def get(self, request, *args, **kwargs):
        obj =  self.custom_get_object()
        return Response(self.get_serializer(obj).data)


    def custom_get_object(self):
        return get_object_or_404(self.get_correct_model(), pk=self.kwargs[next(iter(reversed(self.kwargs)))])


    def create(self, request, *args, **kwargs):

        # valid_input data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # create, update, delete vote
        obj = self.custom_get_object()

        vote = obj.votes.filter(user=self.request.user).first()
        if vote:
            if vote.value == request.data.get('value'):
                obj.votes.remove(vote)
            else:
                vote.value = request.data.get('value')
                vote.save()
        else:
            obj.votes.create(user=self.request.user, value=request.data.get('value'))

        # return post new vote information
        custom_data = self.get(request, *args, **kwargs).data
        headers = self.get_success_headers(custom_data)

        return Response(custom_data, status=status.HTTP_201_CREATED, headers=headers)

    def get_correct_model(self):
        """ Dynamically get model from kwargs param.
        """
        return get_model_from_any_app(list(self.kwargs.keys())[-1].split('_')[0])    
