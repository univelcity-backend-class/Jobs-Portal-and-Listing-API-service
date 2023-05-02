from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import generics, authentication, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from .models import Job, CompanyProfile
from .serializers import JobSerializer, CompanyProfileSerializer
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class JobList(APIView):
    authentication_classes= [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        jobs = Job.objects.get(user=request.user)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


