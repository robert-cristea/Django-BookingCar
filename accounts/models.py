from django.db import models
from django.contrib.auth.models import User
import os
import datetime


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_user_profile'
        ordering = ["-created_at"]

    def __str__(self):
        return f'{str(self.id)}_{self.user.username}_profile'
