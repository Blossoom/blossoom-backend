from rest_framework.viewsets import ModelViewSet
from .models import Artwork, Question
from .serializers import GeneralPostSerializer
from utils.functions import get_model_from_any_app


# Create your views here.


class ArtworkViewset(ModelViewSet):

    queryset = Artwork.objects.all()
    serializer_class = GeneralPostSerializer

    def get_serializer_class(self):
        self.serializer_class.Meta.model=get_model_from_any_app(
            self.get_parser_context(self.request).get('view').basename)
        return super().get_serializer_class()


class QuestionViewset(ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = GeneralPostSerializer

    def get_serializer_class(self):
        self.serializer_class.Meta.model=get_model_from_any_app(
            self.get_parser_context(self.request).get('view').basename)
        return super().get_serializer_class()