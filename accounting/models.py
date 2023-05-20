from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ["email"]
    
    objects = UserManager()

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields for profile customization
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    # Add any other fields as per your requirements

    # Add methods or properties for additional profile functionalities as needed
    # Add methods or properties for additional profile functionalities as needed
    
    def __str__(self):
        return self.user.username
