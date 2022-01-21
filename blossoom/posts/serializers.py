from multiprocessing import context
from re import A
from rest_framework import serializers
from votes.serializers import VoteSerializer


class GeneralPostSerializer(serializers.ModelSerializer):

    votes = serializers.SerializerMethodField()

    class Meta:
        model = None
        fields = '__all__'

    def get_votes(self, ins):
        return VoteSerializer(ins, context={'request': self.context.get('request')}).data