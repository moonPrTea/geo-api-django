import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token


login_url = '/api/accounts/login'
logout_url = '/api/accounts/logout'

USER_PASSWORD = '12345678'

"""
testing authorization route with user token,
valid and incorrect data
"""
@pytest.mark.django_db
def test_login(api_client, user):
    response = api_client.post(
        login_url, {
            'username': user.username, 
            'password': USER_PASSWORD
        })
        
    # waiting for 200 code
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data 
    

@pytest.mark.django_db
def test_login_incorrect(api_client, user):
    response = api_client.post(login_url, {
            'username': '39393',
            'password': '9393939'
        })
        
    # waiting for 401 code, because user with this credentials doesnt exists
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_logout(api_client, user):
    token = Token.objects.create(user=user)
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Token {token.key}'
    )

    response = api_client.post(logout_url)
    
    # 200 code because token exists
    assert response.status_code == status.HTTP_200_OK