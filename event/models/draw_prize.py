from django.db import models
from .draw_event import DrawEvent
from .draw_ticket import DrawTicket

class DrawPrize(models.Model):
    RARITY_CHOICES = [
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('special', 'Special'),
        ('legendary', 'Legendary'),
    ]
    
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, null=False)
    image_url = models.URLField(blank=True, null=True)
    stock = models.IntegerField(default=0, null=False)

    event = models.ForeignKey(
        DrawEvent, on_delete=models.CASCADE, related_name="prizes"
    )

    ticket = models.ForeignKey(
        DrawTicket, on_delete=models.SET_NULL, null=True, blank=True, related_name="prizes"
    )

    order_number = models.IntegerField(null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(order_number__gt=0), name="positive_order_number")
        ]

    def __str__(self):
        return f"{self.name} ({self.rarity}) - Event: {self.event.name}"
