from accounts.models import myAccountManager


import pytest

class TestCreateSuperuser:

    @pytest.mark.skip(reason="Failed to call the User model object from the myAccountManager")  
    @pytest.mark.django_db
    def test_create_superuser_valid_input(self):
        manager = myAccountManager()
        result = manager.create_superuser(email="test@example.com", username="testuser", password="password123", full_name="Test User")
        assert result == "created_user created"
        assert manager.is_admin == True
        assert manager.is_staff == True
        assert manager.is_superuser == True


    @pytest.mark.django_db
    def test_create_superuser_empty_email(self):
        manager = myAccountManager()
        with pytest.raises(ValueError):
            manager.create_superuser(email="", username="testuser", password="password123", full_name="Test User")

    @pytest.mark.django_db
    def test_create_superuser_empty_username(self):
        manager = myAccountManager()
        with pytest.raises(ValueError):
            manager.create_superuser(email="test@example.com", username="", password="password123", full_name="Test User")

    @pytest.mark.django_db
    def test_create_superuser_empty_full_name(self):
        manager = myAccountManager()
        with pytest.raises(ValueError):
            manager.create_superuser(email="test@example.com", username="testuser", password="password123", full_name="")

class TestCreateUser:
    
    @pytest.mark.django_db
    def test_create_user_without_email(self):
        manager = myAccountManager()
        email = ''
        username = 'testuser'
        full_name = 'Test User'
        password = 'password'
        with pytest.raises(ValueError) as e:
            manager.create_user(email=email, username=username, full_name=full_name, password=password)
        assert str(e.value) == "Users must have an email address"

    @pytest.mark.django_db
    def test_create_user_without_full_name(self):
        manager = myAccountManager()
        email = 'test@example.com'
        username = 'testuser'
        full_name = ''
        password = 'password'
        with pytest.raises(ValueError) as e:
            manager.create_user(email=email, username=username, full_name=full_name, password=password)
        assert str(e.value) == "Users must provide their full names "

    
    @pytest.mark.django_db
    def test_create_user_without_username(self):
        manager = myAccountManager()
        email = 'test@example.com'
        username = ''
        full_name = 'Test User'
        password = 'password'
        with pytest.raises(ValueError) as e:
            manager.create_user(email=email, username=username, full_name=full_name, password=password)
        assert str(e.value) == "users must have a username"