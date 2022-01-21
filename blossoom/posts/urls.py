from cgitb import lookup
from rest_framework_nested import routers
from .views import ArtworkViewset, QuestionViewset
from votes.views import VoteViewset

router = routers.DefaultRouter()
router.register(r'artworks', ArtworkViewset)
router.register(r'questions', QuestionViewset)


# Nested routers
artwork_nested = routers.NestedDefaultRouter(router, r'artworks', lookup='artwork')
artwork_nested.register(r'votes', VoteViewset)

question_nested = routers.NestedDefaultRouter(router, r'questions', lookup='question')
question_nested.register(r'votes', VoteViewset)



from django.urls import path, include

urlpatterns = [
    path(r'api/v1/', include(artwork_nested.urls)),
    path(r'api/v1/', include(question_nested.urls)),

]