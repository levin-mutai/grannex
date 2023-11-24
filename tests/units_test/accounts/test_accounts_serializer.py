
from django.db import IntegrityError
import pytest
from rest_framework import serializers
from accounts.serializers import UserRegistrationSerializer
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_user_with_valid_data():
    '''Create a user with valid data and ensure it is saved to the database'''
    serializer = UserRegistrationSerializer()
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "password123"
    }
    user = serializer.create(data)
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    assert user.full_name == "Test User"
    assert user.check_password("password123")



@pytest.mark.django_db
def test_create_user_with_valid_data_missing_fields():
    '''Create a user with missing fields and ensure it raises a validation error'''
    serializer = UserRegistrationSerializer()
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    }
    with pytest.raises(KeyError):
        serializer.create(data)

@pytest.mark.django_db
def test_create_user_with_duplicate_email():
    '''Create a user with a duplicate email and ensure it raises a validation error'''
    serializer = UserRegistrationSerializer()
    data1 = {
        "username": "testuser1",
        "email": "testuser@example.com",
        "full_name": "Test User 1",
        "password": "password123"
    }
    data2 = {
        "username": "testuser2",
        "email": "testuser@example.com",
        "full_name": "Test User 2",
        "password": "password123"
    }
    serializer.create(data1)
    with pytest.raises(IntegrityError):
        serializer.create(data2)
    