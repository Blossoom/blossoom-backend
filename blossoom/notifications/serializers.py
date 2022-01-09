from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Notification


class NotificationSerializer(ModelSerializer):

    sender = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()


    class Meta:
        model = Notification
        fields = ('id', 'sender', 'target', 'message', 'timestamp', 'notification_type')
    
    def get_sender(self, notification):
        """
        Return basic information about the sender
        """
        sender = notification.sender
        return {
                'id': sender.id,
                'username': sender.profile.username,
                'profile_pic': str(sender.profile.profile_pic)
        }

    def get_target(self, notification):
        """
        Return id from where the notification is triggered
        """
        return (
            notification.trigger.id
            if notification.notification_type != 'fl'
            else notification.trigger.follow_to.id
        )

    def get_message(self, notification):
        messages = {
            "fl": "started following you",
            "lk": "liked your post",
            "cm": "commented on your post"
        }

        return f"{notification.sender.username} {messages[notification.notification_type]}"