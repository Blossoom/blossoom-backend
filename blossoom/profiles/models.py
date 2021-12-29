from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    bio = models.TextField(default="No bio yet :)")
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(blank=True, null=True, default='default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_verified = models.BooleanField(default=False)
    collab_status = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return f"@{self.username}"