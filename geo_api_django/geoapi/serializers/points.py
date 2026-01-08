from rest_framework import serializers
from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.gis.measure import D

from ..models import Point

class InputPointCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    
    '''
    describes what model, fields will be used 
    and how this object will be saved. 
    Fields: what fields will be in request, in what order
    ''' 
    
    # validate input values
    def validate(self, attrs):
        input_latitude = attrs['latitude']
        input_longitude = attrs['longitude']
        
        if not (-90 <= input_latitude <= 90):
            raise serializers.ValidationError('Incorrect latitude')
        if not (-180 <= input_longitude <= 180):
            raise serializers.ValidationError('Incorrect longitude')
        
        new_location = GeoPoint(input_longitude, input_latitude, srid=4326)
        
        # checking for duplicate data
        check_exists = Point.objects.filter(
            location__distance_lte=(new_location, D(m=1)),
            title=attrs['title']
        ).exists()
        
        if check_exists:
            raise serializers.ValidationError({
                'location field': f'point with current location: ({input_latitude}, {input_longitude}) and title already exists'
            })
        
        return attrs
    
    def create(self, validated_data):
        request = self.context['request']
        
        input_latitude = validated_data.pop('latitude')
        input_longitude = validated_data.pop('longitude')
        
        # include common geo field with srid - 4326
        validated_data['location'] = GeoPoint(
            input_longitude,
            input_latitude, 
            srid=4326
        )
        
        point = Point.objects.create(
            title=validated_data['title'],
            location=validated_data['location'],
            creator=self.context['request'].user
        )
        
        return point


class OutputPointCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    creator = serializers.CharField(source='creator.username')
    created_at = serializers.DateTimeField()
    
    def get_latitude(self, obj):
        return obj.location.y
    
    def get_longitude(self, obj):
        return obj.location.x


'''
serializers for search point routes,
InputSearchPointSerializer for search params, returns GeoPoint
OutputSearchPointSerializer returns search results
'''
class InputSearchPointSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius = serializers.FloatField(
        required=True, 
        help_text="radius in km"
    )
    
    def validate(self, attrs):
        input_latitude = attrs['latitude']
        input_longitude = attrs['longitude']
        
        if not (-90 <= input_latitude <= 90):
            raise serializers.ValidationError('Incorrect latitude')
        if not (-180 <= input_longitude <= 180):
            raise serializers.ValidationError('Incorrect longitude')
        
        return attrs
    
    def create_geo_points(self, validated_data):
        return GeoPoint(
            self.validated_data['longitude'],
            self.validated_data['latitude'],
            srid=4326
        )


class OutputSearchPointSerializer(serializers.Serializer):
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    creator = serializers.CharField(source='creator.username')
    created_at = serializers.DateTimeField()
    
    def get_latitude(self, obj):
        return obj.location.y if obj.location else None
    
    def get_longitude(self, obj):
        return obj.location.x if obj.location else None
    
    # for tests
    def get_title(self, obj):
        return obj.title if obj.title else None
    
    def get_distance(self, obj):
        if hasattr(obj, 'distance_metres'):
            return obj.distance.m / 1000 if hasattr(obj.distance, 'm') else obj.distance / 1000
        if hasattr(obj, 'distance'):
            return obj.distance_km
        
        return None