from rest_framework import routers
from .views import NotificationViewset

router = routers.DefaultRouter()
router.register('notifications', NotificationViewset)