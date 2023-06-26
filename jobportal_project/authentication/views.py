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
from .serializers import UserSerializer
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