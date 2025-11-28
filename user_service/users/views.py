import traceback
import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserCreateSerializer

logger = logging.getLogger(__name__)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            # Use the create serializer for input validation and creation
            create_serializer = UserCreateSerializer(data=request.data)
            create_serializer.is_valid(raise_exception=True)
            user = create_serializer.save()
            
            # Return the full user data using the regular serializer
            response_serializer = UserSerializer(user)
            headers = self.get_success_headers(response_serializer.data)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        except ValidationError as e:
            # Handle duplicate username gracefully without logging spam
            if 'username' in e.detail and 'already exists' in str(e.detail):
                # Return 409 Conflict for duplicate username (common in load tests)
                return Response(
                    {'error': 'Username already exists', 'code': 'duplicate_username'}, 
                    status=status.HTTP_409_CONFLICT
                )
            logger.warning(f"Validation error: {e.detail}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        except IntegrityError as e:
            # Database-level constraint violation (race condition)
            logger.warning(f"Integrity error during user creation: {str(e)}")
            return Response(
                {'error': 'Username already exists', 'code': 'duplicate_username'}, 
                status=status.HTTP_409_CONFLICT
            )
        
        except Exception as e:
            # Unexpected errors
            logger.error(f"Unexpected error creating user: {e}")
            logger.error(f"Request data: {request.data}")
            traceback.print_exc()
            return Response(
                {'error': 'Internal server error', 'detail': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
    except Exception as e:
        print(f"Error retrieving user by ID: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
