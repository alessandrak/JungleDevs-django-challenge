from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import login, get_user_model

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import LoginSerializer, SignUpSerializer

User = get_user_model()


class LoginAPIView(APIView):
	permission_classes = [AllowAny]
	serializer_class = LoginSerializer

	@swagger_auto_schema(request_body=LoginSerializer, responses={200: openapi.Response('')})
	def post(self, request):
		serializer_class = self.get_serializer_class()
		serializer = serializer_class(data=request.data)
		if serializer.is_valid():
			user = serializer.validated_data['user']
			login(request, user)
			return Response(status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class SignUpCreateAPIView(generics.CreateAPIView):
	queryset = User.objects.all()
	permission_classes = [AllowAny]
	serializer_class = SignUpSerializer
