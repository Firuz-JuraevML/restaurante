from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Restaurant, Review, Reply, UserEdit
from datetime import timedelta 

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password', 
            'role',
            'uid'
        )

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        #print (user)
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            
            # refresh_token = str(refresh)
            # access_token = str(refresh.access_token)
            access_token = refresh.access_token
            access_token.set_exp(lifetime=timedelta(days=1))

            update_last_login(None, user)

            validation = {
                # 'access': access_token,
                'access': str(access_token), 
                'refresh': str(refresh),
                'email': user.email,
                'role': user.role
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'uid',
            'email',
            'role'
        )


class UserEditSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = UserEdit
        fields = (
            'user_uid', 
            'email'
        )
#------------------------------Restaurants--------------------------------#

class RestaurantSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Restaurant 
        fields = (
            'owner', 
            'restaurant_name', 
            'description', 
            'id',
            'overall_rating', 
            'unread_reviews'
        )


class RestaurantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'owner', 
            'restaurant_name', 
            'description'
        )

    def create(self, validated_data):
        restaurant = Restaurant.objects.create(**validated_data)
        return restaurant



#------------------------------Reviews--------------------------------#

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'id',
            'author', 
            'restaurant', 
            'rate', 
            'date_of_visit', 
            'comment', 
            'has_reply', 
            'reply_text'
        )


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'author', 
            'restaurant', 
            'rate', 
            'date_of_visit', 
            'comment'
        )

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)
        return review


#------------------------------Reply--------------------------------#

class ReplyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = (
            'id',
            'review',
            'reply_text',
            'date_of_reply'
        )


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = (
            'review', 
            'reply_text', 
            'date_of_reply'
        )

    def create(self, validated_data):
        reply = Reply.objects.create(**validated_data)
        return reply