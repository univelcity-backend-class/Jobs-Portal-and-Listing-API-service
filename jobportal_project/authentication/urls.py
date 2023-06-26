from django.urls import path
from .views import UserCreate, JobCreateView, CompanyCreateView, JobUpdateView, JobDeleteView, RecentJobsListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', UserCreate.as_view(), name='signup'),
    path('jobs/user/<str:username>/', UserJobsListView.as_view(), name='user-jobs'),
    path('company-create/', CompanyCreateView.as_view(), name='company creation'),
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_view'),
    path('job-delete/<int:job_id>/', JobDeleteView.as_view(), name= 'Job delete'),
    path('jobs/recent/', RecentJobsListView.as_view(), name='recent-jobs'),
    path('update-job/<int:job_id>/', JobUpdateView.as_view(), name='Job info update'),
    path('login/token/refresh', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('job-create/', JobCreateView.as_view(), name='job creation')
 ]