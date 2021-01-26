import uuid

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone

from .managers import CustomUserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

    # These fields tie to the roles!
    ADMIN = 1
    MANAGER = 2
    EMPLOYEE = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Owner'),
        (EMPLOYEE, 'RugularUser')
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=7)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.EmailField()
    modified_by = models.EmailField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserEdit(models.Model): 
    user_uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    email = models.EmailField(unique=True)

class Restaurant(models.Model):
    owner = models.ForeignKey(User, to_field='uid', on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    overall_rating = models.FloatField(default=0.0) 
    unread_reviews = models.IntegerField(default = 0)

    def __str__(self):
        return self.restaurant_name



class Review(models.Model):
    author = models.ForeignKey(User, to_field='uid', on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, to_field='id', on_delete=models.CASCADE)
    rate = models.IntegerField(default = 5)
    date_of_visit = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)

    has_reply = models.BooleanField(default=False)
    reply_text = models.TextField(default="")




class Reply(models.Model):
    review = models.ForeignKey(Review, to_field='id', on_delete=models.CASCADE)
    reply_text = models.TextField()
    date_of_reply = models.DateTimeField(auto_now_add=True) 