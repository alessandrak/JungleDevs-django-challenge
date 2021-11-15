from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('articles', views.ArticleReadOnlyViewSet, basename='articles')
router.register('admin/articles', views.ArticleAdminViewSet, basename='admin-articles')

urlpatterns = [
    path('api/', include(router.urls))
]