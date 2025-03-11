
from django.db import models

class DrawEvent(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=255, null=False, blank=False)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_prizes = models.IntegerField(null=False)
    remaining_prizes = models.IntegerField(null=False)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"
