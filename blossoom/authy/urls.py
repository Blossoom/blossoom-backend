from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import RegisterUser, Logout

urlpatterns = [
    # Your URLs...
    path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', Logout.as_view(), name='logout-blacklist'),
    path('auth/register', RegisterUser.as_view(), name='user-registration')
]