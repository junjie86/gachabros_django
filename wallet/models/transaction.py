from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('c', 'Credit'),
        ('d', 'Debit'),
    ]

    CURRENCY_TYPES = [
        ('real_money', 'Real Money'),
        ('bonus_points', 'Bonus Points'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')

    type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=20, choices=CURRENCY_TYPES)

    related_transaction = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='related_transactions'
    )

    last_balance = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.type} {self.amount} {self.currency} (User: {self.user.username})"
