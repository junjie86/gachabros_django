from django.db import models
from django.contrib.auth.models import User
from core.models.profile import Profile

class Wallet(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='wallet')

    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bonus_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    locked_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_transaction_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet of {self.user.user.username} - Balance: {self.balance}"