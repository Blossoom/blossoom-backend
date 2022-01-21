from difflib import restore
from django.apps import AppConfig
from rest_framework.viewsets import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


from django.contrib.auth import get_user_model
from .serializers import RegisterUserSerializer


class RegisterUser(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny, )


class Logout(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        #try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
        #except Exception as e:
        #    print(e.__traceback__.__str__)
        #    return Response(status=status.HTTP_400_BAD_REQUEST)