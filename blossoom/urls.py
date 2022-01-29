"""blossoom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from articles.urls import router as article_router
from django.conf import settings  # add this
from django.conf.urls.static import static  # add this
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Endpoints

from Events.urls import router as event_router
from notifications.urls import router as notification_router
from posts.urls import router as posts_router
from profiles.urls import router as profile_router
from tags.urls import router as tag_router

# API docs
from rest_framework import permissions
from rest_framework_nested.routers import DefaultRouter

api_router = DefaultRouter()
api_router.registry.extend(profile_router.registry)
api_router.registry.extend(notification_router.registry)
api_router.registry.extend(posts_router.registry)
api_router.registry.extend(article_router.registry)
api_router.registry.extend(event_router.registry)
api_router.registry.extend(tag_router.registry)


schema_view = get_schema_view(
   openapi.Info(
      title="Blossoom API",
      default_version='v1',
      description="Try our api",
      terms_of_service="https://www.google.com/policies/terms/",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_router.urls)),
    path('api/v1/auth/', include('authy.urls')),
    
    # nested routers
    path('', include('posts.urls')),
    path('', include('articles.urls')),


   path(r'', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
