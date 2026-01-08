import random
import pytest
from rest_framework import status
from django.contrib.gis.geos import Point as GeoPoint
from rest_framework.authtoken.models import Token

from ..models import Point, Message


create_message_url = '/api/points/messages'


@pytest.mark.django_db
def test_create_message(auth_client, user):
    point = Point.objects.create(
        title='New example point',
        location=GeoPoint(1.9494, -4.129),
        creator=user
    )
    
    count_messages = Message.objects.count()
    
    response = auth_client.post(create_message_url, {
        'id_point': point.id,
        'message_text': 'happy new year!'
    })

    assert response.status_code == status.HTTP_200_OK
    assert Message.objects.count() == count_messages + 1
    
    # verify message data
    message = Message.objects.first()
    assert message.creator == user
    assert message.point == point
    assert message.message_text == 'happy new year!'

    # check response data
    data = response.data['object']
    assert data['id_point'] == point.id
    assert data['point_title'] == 'New example point'
    assert data['creator_username'] == user.username


# test without token
@pytest.mark.django_db
def test_create_message_unauthorized(api_client):
    response = api_client.post(create_message_url, {
        'id_point': 1,
        'message_text': 'example text'
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

# test with invalid point id
@pytest.mark.django_db
def test_create_message_invalid_point(auth_client):
    response = auth_client.post(create_message_url, {
        'id_point': 949494,
        'message_text': 'example text'
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# test with empty message text
@pytest.mark.django_db
def test_create_message_empty_text(auth_client, user):
    point = Point.objects.create(
        title='Point',
        location=GeoPoint(1.9494, -4.129),
        creator=user
    )

    response = auth_client.post(create_message_url, {
        'id_point': point.id,
        'message_text': '   '
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'message_text' in response.data
    

# test with empty message text
@pytest.mark.django_db
def test_create_message_missing_text(auth_client, user):
    point = Point.objects.create(
        title='Point',
        location=GeoPoint(1.9494, -4.129),
        creator=user
    )

    response = auth_client.post(create_message_url, {
        'id_point': point.id
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST
