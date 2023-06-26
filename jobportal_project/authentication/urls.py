from django.urls import path
from .views import UserCreate, JobCreateView, CompanyCreateView, JobUpdateView, JobDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', UserCreate.as_view(), name='signup'),
    path('company-create/', CompanyCreateView.as_view(), name='company creation'),
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_view'),
    
    path('update-job/<int:job_id>/', JobUpdateView.as_view(), name='Job info update'),
    path('login/token/refresh', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('job-create/', JobCreateView.as_view(), name='job creation')
 ]