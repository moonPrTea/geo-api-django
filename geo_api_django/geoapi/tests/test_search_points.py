import random
import pytest
from django.contrib.gis.geos import Point as GeoPoint
from rest_framework import status
from rest_framework.authtoken.models import Token

from ..models import Point


points_search_url = '/api/points/search'


@pytest.mark.django_db
def test_search_points(api_client, user):
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
    # create point to search
    Point.objects.create(
        title='test point',
        location=GeoPoint(-20.7372, 41.32),
        creator=user
    )
    
    response = api_client.get(points_search_url, {
        'radius': 1,
        'latitude': 41.32,
        'longitude': -20.7372
    })
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count_points'] == 1
    assert isinstance(response.data['points'], list)
    assert response.data['points'][0]['title'] == 'test point'


# test without token
@pytest.mark.django_db
def test_search_points_unathorizated(api_client):
    response = api_client.get(points_search_url, {
        'radius': 10,
        'latitude': -20.7372,
        'longitude': 41.32
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# test with invalid location data
@pytest.mark.django_db
def test_search_invalid_points(api_client, user):
    token = Token.objects.create(user=user)
    api_client.credentials(
        HTTP_AUTHORIZATION=f"Token {token.key}"
    )
    
    response = api_client.get(points_search_url, {
        'radius': 1,
        'latitude': random.uniform(90, 250),
        'longitude': random.uniform(250, 500)
    })
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    
# test without required params
@pytest.mark.django_db
def test_search_points_without_params(auth_client):
    response = auth_client.get(points_search_url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    