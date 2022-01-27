from profiles.serializers import BasicUserDisplaySerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Notification


class NotificationSerializer(ModelSerializer):

    sender = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()
    timesince = serializers.ReadOnlyField(source='FORMAT')


    class Meta:
        model = Notification
        fields = ('id', 'sender', 'detail', 'timesince')
    
    def get_sender(self, notification):
        """
        Return basic information about the sender
        """
        sender = notification.sender
        return BasicUserDisplaySerializer(sender.profile, context={'request': self.context.get('request')}).data

    def get_detail(self, notification):
        """
        Return detail about notification
        """
        action_on = notification.trigger.post.__class__.__name__.lower() if notification.notification_type != 'follow' else 'profile'
        messages = {
            "follow": "started following you",
            "upvote": "upvoted your " + action_on,
            "downvote": "downvoted your " + action_on,            
            "comment": "commented on your " + action_on
        }

        data = {
            'target': {
                'type': action_on,
                'id': notification.trigger.follow_to.id if action_on == 'profile'
                    else notification.trigger.post.post.id if action_on == 'comment'
                    else notification.trigger.post.id
            },

            'message': f"{notification.sender} {messages[notification.notification_type]}"
        }

        return data


        

