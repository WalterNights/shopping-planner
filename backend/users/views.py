from .models import *
from .serializer import *
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        data = request.data.copy()
        user_profile_data = {}
        for key in data:
            values =data.getlist(key)
            if len(values) == 1 and not hasattr(values[0], 'read'):
                user_profile_data[key] = values[0]
            else:
                user_profile_data[key] = values
        try:
            profile = user.userprofile
            serializer = UserDetailSerializer(profile, data=user_profile_data, partial=True)
        except UserProfile.DoesNotExist:
            serializer = UserDetailSerializer(data=user_profile_data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("❌ Errors to serializer:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserProfileCheckView(APIView):
    permission_classes =[IsAuthenticated]
    
    def get(self, request):
        profile = request.user.userprofile
        if not profile.number_id or not profile.phone or not profile.city or not profile.address:
            return Response({'complete': False}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'complete': True}, status=status.HTTP_200_OK)
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user_id'] = user.id
        data['username'] = user.username
        data['email'] = user.email
        data['rol'] = user.rol
        return data
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer