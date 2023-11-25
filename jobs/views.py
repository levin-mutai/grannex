from rest_framework import viewsets, status,pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import *
from .models import *
from grannex.permisions import IsAdminUserOrIsAuthenticatedReadOnly

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class LargePagination(pagination.PageNumberPagination):
    """Class for custom Pagination"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class JobsViewSet(viewsets.ModelViewSet):

    serializer_class = JobSerializer
    queryset = Jobs.objects.all()
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class =LargePagination
    permission_classes = [IsAdminUserOrIsAuthenticatedReadOnly]

    def get_queryset(self):
        return self.queryset
    
  
    
    def get_my_jobs(self, request):
        user = request.user
        return Jobs.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
       
        
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    @method_decorator(cache_page(60 * 15, key_prefix="IP_LISTS"))
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request,pk=None, *args, **kwargs):
       
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    def destroy(self, request,pk=None, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ApplicantsViewSet(viewsets.ModelViewSet):

    serializer_class = ApplicantPostSerializer
    queryset = Applicants.objects.all()
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = LargePagination
    def get_queryset(self):
        return self.queryset
    
  
    
    
    def get_my_applicantions(self, request):
        user = request.user
        applications = Applicants.objects.filter(user=user)

        return Response(ApplicantsSerializer(applications, many=True).data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
       
        serializer = ApplicantsSerializer(queryset, many=True,context={"request": request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = ApplicantSerializer(instance,context={"request": request})
        return Response(serializer.data)
    
    def get_my_applicantions(self, request, job_id=None, *args, **kwargs):

        applications = Jobs.objects.get(id=job_id).get_applicants();


        return Response(ApplicantsSerializer(applications, many=True).data)
    
    def update(self, request,pk=None, *args, **kwargs):
        user = request.user
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial,context={"request": request})
        serializer.is_valid(raise_exception=True)
        if user.id == instance.user.id: # check to ensure that the applicant is the one updating the application.
        
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        

        
    
    def destroy(self, request,pk=None, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if user.id == instance.user.id: # ensure the applicant is the one deleting job application
            self.perform_destroy(instance)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_204_NO_CONTENT)
    



    

    """
    {
  "company": "Safaricom",
  "location": "Nairobi,Kenya",
  "url": "https://carrier.safaricom.com",
  "application_deadline": "2023-11-27",
  "description": "Justa normal job, you should all appy",
  "title": "Software Engineer",
  "category": 0
}
    
    """