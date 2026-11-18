from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ('email', 'password', 'phone_number', 'birthdate')

    def validate_phone_number(self, value):
        if value and not str(value).startswith('996'):
            raise serializers.ValidationError("Номер телефона должен начинаться с 996.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Неверный email или пароль.')
        else:
            raise serializers.ValidationError('Необходимо указать email и пароль.')
        
        data['user'] = user
        return data

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['birthdate'] = str(user.birthdate) if user.birthdate else None
        return token