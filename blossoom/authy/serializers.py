from rest_framework import serializers
from django.contrib.auth.models import User


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
        email = User.objects.filter(email=data.get('email')).exists()
        if email:
            raise serializers.ValidationError({"email": "user with this email already exists."})

        return super().validate(data)

    def create(self, validated_data):
        
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
