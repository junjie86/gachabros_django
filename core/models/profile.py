from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('locked', 'Locked'),
        ('banned', 'Banned'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    referer_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_profiles')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
