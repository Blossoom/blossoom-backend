from profiles.serializers import BasicUserDisplaySerializer
from rest_framework import serializers
from votes.serializers import VoteSerializer

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    user = BasicUserDisplaySerializer(source='user.profile', read_only=True)
    timesince = serializers.ReadOnlyField(source="FORMAT")
    votes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment 
        exclude = ('content_type', 'object_id', 'created', 'updated')

    def get_votes(self, ins):
        return VoteSerializer(ins, context={'request': self.context.get('request')}).data
