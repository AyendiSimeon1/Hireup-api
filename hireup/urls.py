from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from core.views import RegisterView, LoginView

shema_view = get_schema_view (
    openapi.Info (
        title = 'Hireup Api',
        default_version = 'v1',
        description = 'Api Endpoints for Hireup',

    ),
    public=True,
    permission_classes = (permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('accounts/', include('allauth.urls')),
    path('', shema_view.with_ui('swagger', cache_timeout=0), name='shema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', shema_view.without_ui(cache_timeout=0), name='schema-json'),
]
