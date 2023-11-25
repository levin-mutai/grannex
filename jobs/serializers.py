from rest_framework import serializers
from .models import *
from accounts.serializers import UserListSerializer


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = '__all__'

class ApplicantPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicants
        fields = '__all__'
    
    

class ApplicantsSerializer(ApplicantPostSerializer):
    user = UserListSerializer(read_only=True)
    class Meta:
        model = Applicants
        fields = '__all__'
    
    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)
    
        
        
class ApplicantSerializer(ApplicantsSerializer):
    job = JobSerializer(read_only=True)
    class Meta:
        model = Applicants
        fields = '__all__'
    def get_photo_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)
