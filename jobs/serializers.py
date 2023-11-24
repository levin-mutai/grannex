from rest_framework import serializers
from .models import *
from accounts.serializers import UserListSerializer


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = '__all__'

class ApplicantsSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    class Meta:
        model = Applicants
        fields = '__all__'
        
class ApplicantSerializer(ApplicantsSerializer):
    job = JobSerializer(read_only=True)
    class Meta:
        model = Applicants
    