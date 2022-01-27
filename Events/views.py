from crypt import methods

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event
from .serializers import EventSerializer

# Create your views here.


class EventViewset(viewsets.ModelViewSet):

    queryset = Event.objects.all().order_by('-created')
    serializer_class = EventSerializer


    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(methods=['get'], detail=True)
    def attend(self, request, pk=None):

        signed_in_user = request.user if not request.user.is_anonymous else None
        if not signed_in_user:
            return Response({ "detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        event = get_object_or_404(Event, pk=pk)
        
        if  signed_in_user.event_attend.filter(id=event.id).exists():
            signed_in_user.event_attend.remove(event)
            return Response({"detail": "Unattend success."}, status=status.HTTP_200_OK)
        else:
            signed_in_user.event_attend.add(event)
            return Response({"detail": "Attend success."}, status=status.HTTP_200_OK)

        