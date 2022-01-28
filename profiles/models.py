from django.contrib.auth.models import User
from django.db import models

# overwrite attributes.

User._meta.get_field('email')._unique = True

def upload_to(instance, filename):
    return "profiles/{}".format(filename)


class Profile(models.Model):

    # Link extending default user model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    
    # Basic user information
    username = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to=upload_to, default='default.png')
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
    is_new = models.BooleanField(default=True)

    tags = models.ManyToManyField('tags.Tag', related_name='profile_tags', blank=True)


    # Relational fields
    # profile.followers
    # profile.followings

    def __str__(self) -> str:
        return f"@{self.username}"
