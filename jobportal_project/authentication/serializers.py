from django.contrib.auth.models import User
from rest_framework import serializers
from .models import CompanyProfile, Job

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs= {'password': {'write_only': True}}

    

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return {
            'username': user.username,
            'email': user.email
        }




class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ('id', 'company_name', 'company_description', 'location', 'website', )


class JobSerializer(serializers.ModelSerializer):
    company = CompanyProfileSerializer()

    class Meta:
        model = Job
        fields = ('id', 'title', 'description', 'company', )

