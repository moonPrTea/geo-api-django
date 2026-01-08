from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import Point
from ..serializers import (
    InputPointCreateSerializer, OutputPointCreateSerializer,
    InputSearchPointSerializer, OutputSearchPointSerializer
    )


'''
view for creating points on map
input: title, latitude, longitude
output: status, message, point values
'''
class PointsCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InputPointCreateSerializer(
            data = request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        new_point = serializer.save()
        
        output_serializer = OutputPointCreateSerializer(new_point)
        return Response({
            'message': 'point successfully created',
            'object': output_serializer.data
        })


'''
view to search points in some input radius
input: latitude, longitude, radius(kilometers)
output: found data
'''
class PointsSearchApi(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = InputSearchPointSerializer(
            data = request.query_params,
            context ={'request': request}
        )
        
        print(request.query_params)
        
        if not serializer.is_valid():
            return Response({
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        latitude = validated_data['latitude']
        longitude = validated_data['longitude']
        radius = validated_data['radius']
        
        # central point for search operation
        central_point = serializer.create_geo_points(validated_data) 
        try:
            # filter points with location close to input (considering radius)
            points = Point.objects.filter(
                location__distance_lte=(central_point, Distance(km=radius))
            ).annotate(
                distance_metres=DistanceFunction('location', central_point) 
            ).order_by('distance_metres') 
            
            for point in points:
                point.distance = point.distance_metres / 1000 # metres to kilometres
            
            output_values = OutputSearchPointSerializer(points, many=True)
            
            # checking empty result
            search_points = output_values.data
            
            return Response({
                'params': {
                    'latitude': latitude,
                    'longitude': longitude,
                    'radius': f"{radius} km"
                }, 
                'count_points': points.count(),
                'points': search_points
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e)
            return Response({
                'message': f'An error occured while processing: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)