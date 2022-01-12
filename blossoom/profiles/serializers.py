from inspect import currentframe
from rest_framework import serializers

from .models import Profile


class RelationStatusSerializer(serializers.ModelSerializer):
    """
    Relationship status between users
    """

    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('is_following', )

    def to_representation(self, instance):
        ret = super(RelationStatusSerializer, self).to_representation(instance)
        if ret["is_following"] is None:
           del ret['is_following']
        return ret
    
    def get_is_following(self, profile):
        current_user = self.context['request'].user
        return None if current_user.profile == profile else current_user.profile.following.filter(follow_to=profile).exists()


class BasicUserDisplaySerializer(RelationStatusSerializer, serializers.ModelSerializer):
    """
    Display basic user information.
    """

    class Meta:
        model = Profile
        fields = ('id', 'username', 'profile_pic', 'bio') + RelationStatusSerializer.Meta.fields



class ProfileSerializer(RelationStatusSerializer, serializers.ModelSerializer):
    
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        exclude = ('user',)
        extra_kwargs = {field: {'read_only':True} for field in RelationStatusSerializer.Meta.fields}

    def get_followers_count(self, profile):
        return profile.followers.all().count()

    def get_followings_count(self, profile):
        return profile.following.all().count()