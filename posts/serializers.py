from multiprocessing import context
from re import A

from profiles.serializers import BasicUserDisplaySerializer
from rest_framework import serializers
from votes.serializers import VoteSerializer


class GeneralPostSerializer(serializers.ModelSerializer):

    user = BasicUserDisplaySerializer(source='user.profile', read_only=True)
    votes = serializers.SerializerMethodField()
    timesince = serializers.ReadOnlyField(source='FORMAT')
    saves = serializers.SerializerMethodField()

    class Meta:
        model = None
        exclude = (
            'created',
            'updated',
        )
    
    def get_votes(self, ins):
        return VoteSerializer(ins, context={'request': self.context.get('request')}).data
    
    def get_saves(self, ins):
        return {
            'has_saved': True if self.context.get('request').user in ins.saves.all() else False,
            'total_saves': ins.saves.all().count()
        }