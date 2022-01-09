from inspect import currentframe
from rest_framework import serializers

from .models import Profile


class BasicRelationSerializer(serializers.ModelSerializer):
    
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('followers_count', 'followings_count', 'is_following')

    def to_representation(self, instance):
        ret = super(BasicRelationSerializer, self).to_representation(instance)
        if ret["is_following"] is None:
           del ret['is_following']
        return ret

    def get_followers_count(self, profile):
        return profile.followers.all().count()

    def get_followings_count(self, profile):
        return profile.following.all().count()
    
    def get_is_following(self, profile):
        current_user = self.context['request'].user
        return None if current_user.profile == profile else current_user.profile.following.filter(follow_to=profile).exists()


class RelationViewSerializer(BasicRelationSerializer, serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'username', 'profile_pic', 'bio') + BasicRelationSerializer.Meta.fields



class ProfileSerializer(BasicRelationSerializer, serializers.ModelSerializer):


    class Meta:
        model = Profile
        exclude = ('user',)
        extra_kwargs = {field: {'read_only':True} for field in BasicRelationSerializer.Meta.fields}



