from django.urls import path
from .views import UserCreate, JobList
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
     path('signup/', UserCreate.as_view(), name='signup'),
     path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_view'),
     path('login/token/refresh', TokenRefreshView.as_view(), name='token_refresh_view'),
     path('profile/', JobList.as_view(), name='profile')

 ]
