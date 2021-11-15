from django_filters.rest_framework import FilterSet

from .models import Article

class ArticleFilterBackend(FilterSet):
    class Meta:
        model = Article
        fields = ('category', )
