from comments.views import CommentViewset
from rest_framework_nested import routers
from votes.views import VoteViewset

from .views import ArtworkViewset, QuestionViewset

# Artwork Question basic routers
router = routers.DefaultRouter()
router.register(r'artworks', ArtworkViewset)
router.register(r'questions', QuestionViewset)


# Nested router add  post votes and comments
artwork_nested = routers.NestedDefaultRouter(router, r'artworks', lookup='artwork')
artwork_nested.register(r'votes', VoteViewset, basename='artwork-votes')
artwork_nested.register(r'comments', CommentViewset, basename='artwork-comments')

# Nested router add votes to  comments
artwork_comment_nested = routers.NestedDefaultRouter(artwork_nested, r'comments', lookup='comment')
artwork_comment_nested.register(r'votes', VoteViewset, basename='a-comment-votes')


question_nested = routers.NestedDefaultRouter(router, r'questions', lookup='question')
question_nested.register(r'votes', VoteViewset, basename='question-votes')
question_nested.register(r'comments', CommentViewset, basename='question-comments')

# Nested router add votes to  comments
question_comment_nested = routers.NestedDefaultRouter(question_nested, r'comments', lookup='comment')
question_comment_nested.register(r'votes', VoteViewset, basename='q-comment-votes')



from django.urls import include, path

urlpatterns = [
    path(r'api/v1/', include(artwork_nested.urls)),
    path(r'api/v1/', include(question_nested.urls)),
    path(r'api/v1/', include(artwork_comment_nested.urls)),
    path(r'api/v1/', include(question_comment_nested.urls)),


]
