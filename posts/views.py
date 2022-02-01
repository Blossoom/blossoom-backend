from django.db.models import Q
from utils.functions import get_model_from_any_app

from .models import Artwork, Question
from .serializers import GeneralPostSerializer
from utils.views import CustomPostModelViewset

# Create your views here.


class ArtworkViewset(CustomPostModelViewset):

    queryset = Artwork.objects.all()
    serializer_class = GeneralPostSerializer

    def get_serializer_class(self):
        self.serializer_class.Meta.model=get_model_from_any_app(
            self.get_parser_context(self.request).get('view').basename)
        return super().get_serializer_class()


class QuestionViewset(CustomPostModelViewset):

    queryset = Question.objects.all()
    serializer_class = GeneralPostSerializer


    def get_serializer_class(self):
        self.serializer_class.Meta.model=get_model_from_any_app(
            self.get_parser_context(self.request).get('view').basename)
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def get_queryset(self):
        query = self.request.query_params.get('q') or ''
        query = query if query in ['hot', 'relevant', 'latest'] else ''

        # TODO: This part need to be redesigned

        # get posts related to user
        posts = super().get_queryset().order_by('-created')

        if not self.request.user.is_anonymous:

            if query == 'relevant':
                posts = posts.filter(Q(user__profile__in=[relationship.follow_to.id for relationship in self.request.user.profile.following.all()])).order_by('-created')
            
        if query == 'hot':
            posts = posts.order_by('-votes', '-created')

        return posts
