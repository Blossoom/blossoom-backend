from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import CustomTokenObtainPairView, Logout, RegisterUser

urlpatterns = [
    # Your URLs...
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', Logout.as_view(), name='logout-blacklist'),
    path('register/', RegisterUser.as_view(), name='user-registration')
]
