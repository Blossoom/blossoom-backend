from django.contrib.auth.models import User, update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings


class RegisterUserSerializer(serializers.ModelSerializer):

    password_2 = serializers.CharField(label="confirm password", min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password_2')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('password_2')
        if password != confirm_password:
            raise serializers.ValidationError({"password": "password and confirm_password didn't match."})
        # email must be unique to each user
        return super().validate(data)

    def create(self, validated_data):
        
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Custom data
        data['profile_id'] = self.user.profile.id
        data['is_new'] = self.user.profile.is_new
        
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
