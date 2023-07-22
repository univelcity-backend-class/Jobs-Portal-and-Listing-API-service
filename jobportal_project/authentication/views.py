from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, authentication, permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from .models import Job, CompanyProfile
from .serializers import JobSerializer, CompanyProfileSerializer
from .serializers import UserSerializer, JobDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

class CompanyCreateView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        account = request.user.id
        account_username = request.user.username
        mutable_data = request.data.copy()
        mutable_data['user'] = account
        mutable_data['username'] = account_username
        serializer = CompanyProfileSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobCreateView(APIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        company = request.user.id
        username = request.user.companyprofile.username
        mutable_data = request.data.copy()
        mutable_data['company'] = company
        mutable_data['company_name'] = username
        serializer = JobSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class JobUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def patch(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"message": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.companyprofile.username == job.company_name:
            serializer = JobSerializer(job, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'you are not authorized to update this job'})
        
class JobDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def delete(self, request, job_id):
        try:
            job = Job.objects.get(id = job_id)
        except Job.DoesNotExist:
            return Response({"message": "Job with this id does not exist."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.companyprofile.username == job.company_name:
            job.delete()
            return Response({"message": "Job deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message':'you are not authorized to delete this post'})
        
class RecentJobsListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        jobs = Job.objects.order_by('-id')[:5]
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    
class UserJobsListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, username):
        jobs = Job.objects.filter(company_name__icontains = username).all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    
class JobFilterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Job.objects.all()

        job_type = request.query_params.get('job_type')
        industry = request.query_params.get('industry')
        category = request.query_params.get('category')
        skill = request.query_params.get('skill')

        if job_type:
            queryset = queryset.filter(job_type__icontains=job_type)
        if industry:
            queryset = queryset.filter(industry__icontains=industry)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if skill:
            queryset = queryset.filter(skill__icontains=skill)

        # Serialize the filtered queryset
        serializer = JobSerializer(queryset, many=True)

        return Response(serializer.data)
    
class JobDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, job_id):
        jobs = Job.objects.get(id=job_id)
        serializer = JobDetailSerializer(jobs)
        return Response(serializer.data)
    
class JobApplicationView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def post(request, job_id):
        try:
            job= Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
