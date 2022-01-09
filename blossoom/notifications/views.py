from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import NotificationSerializer
from .models import Notification

# Create your views here.

class NotificationViewset(ReadOnlyModelViewSet):

    queryset = Notification.objects.filter(seen=False)
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user).order_by('-timestamp')
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.seen = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
