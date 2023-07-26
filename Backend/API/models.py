from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token

# Custom User Model, inheriting from AbstractUser. Right click Abstractuser and go to definition (this works in vscode) for more info on fields
class CustomUser(AbstractUser):
    # Add custom fields to our user model here such as profile_picture_url
    profile_picture_url = models.URLField(blank=True, null=True)
    user_bio = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, null=False)

    # Add any additional methods or properties to the custom user model if needed

    def __str__(self):
        # Return a string representation of the user
        return self.username

User = get_user_model()
