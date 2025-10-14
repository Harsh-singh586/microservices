from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserCreateSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
    def create(self, request, *args, **kwargs):
        # Use the create serializer for input validation and creation
        create_serializer = UserCreateSerializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        user = create_serializer.save()
        
        # Return the full user data using the regular serializer
        response_serializer = UserSerializer(user)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


@api_view(['GET'])
def user_by_id(request, user_id):
    """API endpoint to get user by ID - used by other services"""
    try:
        user = User.objects.get(id=user_id)
        profile = UserProfile.objects.get(user=user)
        profile_serializer = UserProfileSerializer(profile)
        return Response(profile_serializer.data)
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def verify_user(request):
    """API endpoint to verify user credentials - used by other services"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    if user:
        serializer = UserSerializer(user)
        return Response({'valid': True, 'user': serializer.data})
    else:
        return Response({'valid': False, 'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
