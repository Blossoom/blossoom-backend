from profiles.serializers import BasicUserDisplaySerializer
from rest_framework import serializers
from votes.serializers import VoteSerializer

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    
    user = BasicUserDisplaySerializer(source='user.profile', read_only=True)
    votes = serializers.SerializerMethodField(required=False, read_only=True)
    timesince = serializers.ReadOnlyField(source="FORMAT")


    class Meta:
        model = Article
        fields = '__all__'
    
    def get_votes(self, ins):
        return VoteSerializer(ins, context={'request': self.context.get('request')}).data
