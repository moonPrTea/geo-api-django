import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='example',
        password='12345678',
        email='example@example.example'
    )

@pytest.fixture
def auth_client(api_client, user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client



