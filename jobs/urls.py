from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ApplicantsViewSet,JobsViewSet



urlpatterns = [
 
   
    path("applications", ApplicantsViewSet.as_view({"get":"list","post":"create"})),
    path("applications/<id>", ApplicantsViewSet.as_view({"get":"retrieve","put":"update","delete":"destroy"})),
    # path("applications/in/me", ApplicantsViewSet.as_view({"get":"get_my_applicantions"})),

  
    path("", JobsViewSet.as_view({"get":"list","post":"create"})),
    path("<id>", JobsViewSet.as_view({"get":"retrieve","put":"update","delete":"destroy"})),
    path("<job_id>/applicants", ApplicantsViewSet.as_view({"get":"get_my_applicantions"})),

   
]