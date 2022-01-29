from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.

class NotificationViewset(ReadOnlyModelViewSet):

    queryset = Notification.objects.filter(seen=False)
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
        return Notification.objects.filter(recipient=self.request.user).exclude(sender=self.request.user).order_by('-created')
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.seen = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
