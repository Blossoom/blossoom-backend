from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):

    followers = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = '__all__' 


    def get_followers(self, ins):
        return ins.profile_tags.all().count()

    def get_posts(self, ins):
        return ins.article_tags.count() + ins.artwork_tags.count()
    
    def get_is_following(self, ins):
        user = self.context.get('request').user
        user = user.profile if not user.is_anonymous else None
        return ins in user.tags.all() if user else None