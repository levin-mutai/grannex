import pytest
from rest_framework import status

from accounts.views import UserRegistrationView


import pytest
@pytest.mark.django_db
class TestUserRegistrationView:

    def test_valid_registration(self, apiclient):
      
        request_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "password123"
        }
        expected_status = status.HTTP_201_CREATED

   
        response = apiclient.post( "/api/users/register", data=request_data)

    
        assert response.status_code == expected_status
        assert response.data["username"] == request_data["username"]
        assert response.data["email"] == request_data["email"]
        assert response.data["full_name"] == request_data["full_name"]
        assert "password" not in response.data
     
    
    def test_missing_username(self, apiclient):
  
        request_data = {
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "password123"
        }
        expected_status = status.HTTP_400_BAD_REQUEST


        response = apiclient.post( "/api/users/register", data=request_data)


        assert response.status_code == expected_status

 
    def test_missing_email(self, apiclient):
  
        request_data = {
            "username": "testuser",
            "full_name": "Test User",
            "password": "password123"
        }
        expected_status = status.HTTP_400_BAD_REQUEST


        response = apiclient.post( "/api/users/register", data=request_data)


        assert response.status_code == expected_status

    
    def test_missing_password(self, apiclient):
  
        request_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "full_name": "Test User"
        }
        expected_status = status.HTTP_400_BAD_REQUEST


        response = apiclient.post( "/api/users/register", data=request_data)


        assert response.status_code == expected_status
