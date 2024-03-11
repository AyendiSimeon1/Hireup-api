from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

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
   
    path('accounts/', include('allauth.urls')),
    path('core/', include('core.urls')),
    path('', shema_view.with_ui('swagger', cache_timeout=0), name='shema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', shema_view.without_ui(cache_timeout=0), name='schema-json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)