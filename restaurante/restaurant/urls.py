from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserListView,
    UserDeleteView, 
    UserEditView, 
    RestaurantListView, 
    RestaurantCreate,
    ReviewListView,
    ReviewCreateView,
    ReplyCreateView, 
    ReplyListView, 
    ReplyDeleteView,
)

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('users', UserListView.as_view(), name='users'),
    path('users/delete', UserDeleteView.as_view(), name='delete_user'),  
    path('users/edit', UserEditView.as_view(), name='edit_user'),  

    path('restaurants', RestaurantListView.as_view(), name='restaurants'),
    path('restaurants/create', RestaurantCreate.as_view(), name='restaurants_create'),

    path('reviews', ReviewListView.as_view(), name='review_list'),
    path('reviews/create', ReviewCreateView.as_view(), name='review_create'),

    path('replies', ReplyListView.as_view(), name='reply_create'),
    path('reply/create', ReplyCreateView.as_view(), name='reply_create'), 
    path('reply/delete', ReplyDeleteView.as_view(), name='reply_delete')
]