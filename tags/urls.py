from rest_framework import routers
from .views import TagViewset


router = routers.DefaultRouter()
router.register('tags', TagViewset)