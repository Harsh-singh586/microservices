from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('profiles/<int:pk>/', views.UserProfileDetailView.as_view(), name='profile-detail'),
    path('api/user/<int:user_id>/', views.user_by_id, name='user-by-id'),
    path('api/verify/', views.verify_user, name='verify-user'),
]
