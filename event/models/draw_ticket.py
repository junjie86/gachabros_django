
from django.db import models
from core.models.profile import Profile  # Assuming Profile model exists
from .draw_event import DrawEvent
from django.utils import timezone

class DrawTicket(models.Model):
    event = models.ForeignKey(DrawEvent, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='tickets')
    purchased_at = models.DateTimeField(default=timezone.now)
    used = models.BooleanField(default=False)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    def __str__(self):
        return f"Ticket {self.id} for {self.event.name} (User: {self.user.user.username})"
