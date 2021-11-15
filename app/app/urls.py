"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import debug_toolbar

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework.permissions import AllowAny

from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static


schema_view = get_schema_view(
   openapi.Info(
      title='Jungle Devs Challenge API',
      default_version='v1',
      description='Simplified version of a news provider API'
   ),
   public=True,
   permission_classes=(AllowAny, )
)

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('', include('articles.urls')),
    path('', include('authors.urls')),
    path('', include('auth.urls')),
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='docs'),
    
    path('__debug__/', include(debug_toolbar.urls)),

]
