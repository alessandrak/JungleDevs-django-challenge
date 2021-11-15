from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('admin/authors', views.AuthorAdminViewSet, basename='admin-authors')

urlpatterns = [
    path('api/', include(router.urls))
]