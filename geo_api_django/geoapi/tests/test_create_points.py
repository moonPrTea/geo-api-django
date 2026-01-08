import random
import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token

from ..models import Point

points_url = '/api/points'

# test with auth token
@pytest.mark.django_db
def test_create_point(api_client, user):
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
    count_points = Point.objects.count()
    
    created_title = f'example point {str(random.random())}'
    response = api_client.post(points_url, {
        'title': created_title,
        'latitude': random.uniform(-90, 90),
        'longitude': random.uniform(-180, 180)
    })

    assert response.status_code == status.HTTP_200_OK
    assert Point.objects.count() == count_points + 1
    assert response.data['object']['title'] == created_title

# test without token
@pytest.mark.django_db
def test_create_point_unauthorized(api_client):
    response = api_client.post(points_url, {
        'title': 'new cool point',
        'latitude': random.uniform(-90, 90),
        'longitude': random.uniform(-180, 180)
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# test with invalid data, location is not right
@pytest.mark.django_db
def test_create_point_incorrect(api_client, user):
    token = Token.objects.create(user=user)
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Token {token.key}'
    )
    response = api_client.post(points_url, {
        'title': '',
        'latitude': random.uniform(90, 250),
        'longitude': random.uniform(250, 500)
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
