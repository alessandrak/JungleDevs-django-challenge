from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny

from .models import Article
from .filters import ArticleFilterBackend
from .serializers import ArticleReadSerializer, ArticleWriteSerializer, ArticleListSerializer, ArticleBasicRetrieveSerializer


class ArticleAdminViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.select_related('author').defer('created_date', 'updated_date').order_by('-created_date')
	permission_classes = [IsAdminUser]
	filterset_class = ArticleFilterBackend

	def get_serializer_class(self):
		if self.request.method in ['POST', 'PUT', 'PATCH']:
			return ArticleWriteSerializer
		return ArticleReadSerializer


class ArticleReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [AllowAny]
	filterset_class = ArticleFilterBackend

	def get_queryset(self):
		queryset = Article.objects.select_related('author').defer('created_date', 'updated_date').order_by('-created_date')
		# returns the optimized query from the serializer if it exists
		try:
			return self.get_serializer_class().setup_eager_loading(queryset)  
		except AttributeError:
			return queryset

	def get_serializer_class(self):
		if self.action == 'list':
			return ArticleListSerializer
		elif self.request.user.is_authenticated:
			return ArticleReadSerializer
		return ArticleBasicRetrieveSerializer