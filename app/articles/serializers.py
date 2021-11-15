
from rest_framework import serializers

from django.db.models import Prefetch

from .models import Article
from authors.serializers import AuthorSerializer


class ArticleReadSerializer(serializers.ModelSerializer):
    """
    Article serializer for read actions
    """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Article
        exclude = ('created_date', 'updated_date')


class ArticleWriteSerializer(serializers.ModelSerializer):
    """
    Article serializer for write methods (POST, PUT. PATCH)
    """
    class Meta:
        model = Article
        exclude = ('created_date', 'updated_date')


class ArticleListSerializer(ArticleReadSerializer):
    class Meta:
        model = Article
        exclude = ('created_date', 'updated_date', 'first_paragraph', 'body')

    @staticmethod
    def setup_eager_loading(queryset):
        """
        This optimization is important because unnecessary text fields queries
        in the database can be very costly
        """
        return queryset.defer('body', 'first_paragraph')


class ArticleBasicRetrieveSerializer(ArticleReadSerializer):
    class Meta:
        model = Article
        exclude = ('created_date', 'updated_date', 'body')

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.defer('body')