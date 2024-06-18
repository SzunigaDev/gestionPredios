# users/tests.py

import pytest
from django.contrib.auth.models import User, Group, Permission
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def create_superuser():
    superuser = User.objects.create_superuser(username='admin', password='adminpassword')
    return superuser

@pytest.fixture
def get_tokens(create_superuser):
    refresh = RefreshToken.for_user(create_superuser)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@pytest.mark.django_db
def test_user_list(api_client, get_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {get_tokens["access"]}')
    response = api_client.get('/api/users/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_user(api_client, get_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {get_tokens["access"]}')
    response = api_client.post('/api/users/', {
        'username': 'newuser',
        'password': 'newpassword',
        'email': 'newuser@example.com'
    })
    assert response.status_code == 201

@pytest.mark.django_db
def test_group_list(api_client, get_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {get_tokens["access"]}')
    response = api_client.get('/api/groups/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_permission_list(api_client, get_tokens):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {get_tokens["access"]}')
    response = api_client.get('/api/permissions/')
    assert response.status_code == 200
