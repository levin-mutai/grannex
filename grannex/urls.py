"""
URL configuration for grannex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.urls import include


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,

)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework.documentation import include_docs_urls
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header  =  "Grannex"
admin.site.site_title  =  "Grannex"
admin.site.index_title  =  "Grannex"

schema_view = get_schema_view(
    openapi.Info(
        title="GrannexAPI",
        default_version="0.0.1",
        description="""This is an API for Grannex.To access  redoc documentation page please visit ```/redoc```.\n\n For you to use this API you need to first login. You can do that using the user login route(user/login). If not yet a user please register using the user register route(user/register).\n\n After successful login you will get both `access` and `refresh` token. You will need the `access` token for **Authorization**\n\nIf using curl or any other tool make sure to pass `Authorization` as a header with a value of the Bearers token e.g \n\n ```curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk2MzY5MTc2LCJpYXQiOjE2OTYzNjE5NzYsImp"``` """,
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="levinmutai@gmail.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/jobs/", include("jobs.urls")),
    path("api/users/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/users/", include("accounts.urls")),
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        "redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
