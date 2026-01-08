'''
serializers for messages api's.
input<action>Serializer - what data is expected for input
output<action>Serializer - what data will be returned for user
'''
from rest_framework import serializers

from ..models import Point, Message

class InputMessageCreateSerializer(serializers.Serializer):
    message_text = serializers.CharField(required=True)
    id_point = serializers.IntegerField(required=True)
    
    def validate_id_point(self, expected_id):
        if not Point.objects.filter(id=expected_id).exists():
            raise serializers.ValidationError(
                f"point with current id: {expected_id} doesn't exists. "
                "Add new point sending post request on api/points"
            )
        return expected_id
    
    def validate_message_text(self, message):
        # check message text
        if not message.strip():
            raise serializers.ValidationError(
                "message cant be empty. Please write something"
            )
        return message
    
    def create(self, validated_data):
        request = self.context['request']
        point = Point.objects.get(id=validated_data['id_point'])

        return Message.objects.create(
            point=point,
            creator=request.user,
            message_text=validated_data['message_text'].strip()
        )   


class OutputMessageCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    id_point = serializers.IntegerField(source='point.id')
    point_title = serializers.CharField(source='point.title')
    point_coordinates = serializers.SerializerMethodField()
    creator_username = serializers.CharField(source='creator.username')
    message_text = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    
    def get_point_coordinates(self, obj):
        return f"{obj.point.latitude:.6f}, {obj.point.longitude:.6f}"