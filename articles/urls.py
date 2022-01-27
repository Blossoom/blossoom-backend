from re import A

from comments.views import CommentViewset
from rest_framework_nested import routers
from votes.views import VoteViewset

from .views import ArticleViewset

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewset)


# Nested routers add votes && comments
article_nested = routers.NestedDefaultRouter(router, r'articles', lookup='article')
article_nested.register(r'votes', VoteViewset)
article_nested.register(r'comments', CommentViewset, basename='article-comments')

# Nested router add votes to  comments
comment_nested = routers.NestedDefaultRouter(article_nested, r'comments', lookup='comment')
comment_nested.register(r'votes', VoteViewset)



from django.urls import include, path

urlpatterns = [
    path(r'api/v1/', include(article_nested.urls)),
    path(r'api/v1/', include(comment_nested.urls)),

]
