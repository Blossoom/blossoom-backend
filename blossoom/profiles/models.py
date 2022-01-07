from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):

    # Link extending default user model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    
    # Basic user information
    username = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    profile_pic = models.ImageField(blank=True, null=True, default='default.png')
    bio = models.TextField(default="No bio yet :)")
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    background = models.TextField(max_length=200, blank=True, null=True)
    working_on = models.TextField(max_length=200, blank=True, null=True)


    # Backend information
    updated_at = models.DateTimeField(auto_now=True)
    
    # User profile status
    email_verified = models.BooleanField(default=False)
    collab_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"@{self.username}"