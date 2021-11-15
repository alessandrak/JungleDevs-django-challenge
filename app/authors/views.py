from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Author
from .serializers import AuthorSerializer

class AuthorAdminViewSet(viewsets.ModelViewSet):
	queryset = Author.objects.defer('created_date', 'updated_date').order_by('-created_date')
	serializer_class = AuthorSerializer
	permission_classes = [IsAdminUser]