from profiles.serializers import BasicUserDisplaySerializer
from rest_framework import serializers

from Events.models import Event


class EventSerializer(serializers.ModelSerializer):

    user = BasicUserDisplaySerializer(read_only=True, source='user.profile')
    attendees = serializers.SerializerMethodField()
    timesince = serializers.ReadOnlyField(source='FORMAT')
    event_date = serializers.SerializerMethodField()
    

    class Meta:
        model = Event
        exclude = ('created', 'updated')
        extra_kwargs = {
            'date': {
                'write_only': True
            }
        }

    def get_event_date(self, ins):
        return ins.humanized_date()

    def get_attendees(self, ins):
        return {
            'total_attends': ins.total_attendees(),
            'is_attended': self.context.get('request').user.event_attend.filter(id=ins.id).exists()
        }
