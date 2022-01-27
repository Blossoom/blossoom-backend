from dataclasses import field

from rest_framework import serializers

from .models import Vote


class VoteSerializer(serializers.ModelSerializer):

    total_votes = serializers.SerializerMethodField()
    has_voted = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = ('total_votes', 'has_voted', 'user_vote', 'value')
        extra_kwargs = {
            'value': {'write_only': True}
        }
    
    def get_has_voted(self, ins):
        user_vote = ins.votes.filter(user=self.context.get('request').user) if not self.context.get('request').user.is_anonymous else False
        return True if user_vote else False
    
    def get_user_vote(self, ins):
        return None if not self.get_has_voted(ins) else ins.votes.get(user=self.context.get('request').user).value

    def get_total_votes(self, ins):
        return ins.votes.filter(value='upvote').count() - ins.votes.filter(value='downvote').count()
