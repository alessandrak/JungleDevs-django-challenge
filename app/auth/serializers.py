from rest_framework import serializers

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=254, required=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        max_length=128,
        write_only=True,
        required=True
    )

    def validate(self, data):
        user = authenticate(
            request=self.context.get('request'),
            username=data.get('username'), 
            password=data.get('password')
        )
        if not user:
            response = serializers.ValidationError('That username and password combination is incorrect. ', code=401)
            response.status_code = 401
            raise response
        data['user'] = user
        return data


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        max_length=128,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(SignUpSerializer, self).create(validated_data)