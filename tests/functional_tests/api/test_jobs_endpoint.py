from jobs.models import Jobs
from jobs.views import JobsViewSet
from rest_framework import status
from accounts.models import User


import pytest

@pytest.mark.django_db
class TestCreate:

    
    def test_create_single_job_successfully(self, apiclient):
        # Create a user
        user = User.objects.create_user(email="test@email.com", full_name="test user", username='testuser', password='testpassword')
        user.is_admin = True
        user.save()

        
        apiclient.force_authenticate(user)

        request_data = {
            "company": "Google",
            "location": "Mountain View, CA",
            "url": "https://www.google.com",
            "application_deadline": "2023-12-31",
            "description": "Exciting job opportunity at Google",
            "title": "Software Engineer",
            "category": 0
        }

        response = apiclient.post('/api/jobs/', data=request_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        
        job = Jobs.objects.get(pk=response.data['id'])
        assert job.company == "Google"
        assert job.location == "Mountain View, CA"
        
        apiclient.force_authenticate(user=None)

    def test_create_multiple_jobs_successfully(self, apiclient):
       
        user = User.objects.create_user(email="test@email.com", full_name="test user", username='testuser', password='testpassword')
        user.is_admin = True
        user.save()
     
        apiclient.force_authenticate(user)

        request_data = [
            {
                "company": "Google",
                "location": "Mountain View, CA",
                "url": "https://www.google.com",
                "application_deadline": "2023-12-31",
                "description": "Exciting job opportunity at Google",
                "title": "Software Engineer",
                "category": 0
            },
            {
                "company": "Microsoft",
                "location": "Redmond, WA",
                "url": "https://www.microsoft.com",
                "application_deadline": "2023-12-31",
                "description": "Exciting job opportunity at Microsoft",
                "title": "Software Engineer",
                "category": 0
            }
        ]
        response = apiclient.post('/api/jobs/', data=request_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

       
        assert Jobs.objects.count() == len(request_data)

        for idx, job_data in enumerate(request_data):
            job = Jobs.objects.get(pk=response.data[idx]['id'])
            assert job.company == job_data['company']
            assert job.location == job_data['location']
           
       
        apiclient.force_authenticate(user=None)

    
        
    def test_create_single_job_missing_fields(self, apiclient):
        # Create a user
        user = User.objects.create_user(email="test@example.com", full_name="test user", username='testuser', password='testpassword')
        user.is_admin = True
        user.save()
        apiclient.force_authenticate(user)

        request_data = {
            "company": "Google",
            "location": "Mountain View, CA",
            "url": "https://www.google.com",
            # Missing application_deadline field
            "description": "Exciting job opportunity at Google",
            "title": "Software Engineer",
            "category": 0
        }

        response = apiclient.post('/api/jobs/', data=request_data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Clean up (optional)
        apiclient.force_authenticate(user=None)


    