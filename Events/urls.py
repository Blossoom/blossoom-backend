from rest_framework import routers
from .views import EventViewset

router = routers.DefaultRouter()
router.register('events', EventViewset)