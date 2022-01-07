from rest_framework import serializers

from .models import Profile


class RelationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'username', 'profile_pic')



class ProfileSerializer(serializers.ModelSerializer):

    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        exclude = ('user',)

    def get_followers_count(self, profile):
        return profile.followers.all().count()

    def get_followings_count(self, profile):
        return profile.following.all().count()

