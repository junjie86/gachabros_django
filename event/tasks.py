# tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db import connection
from event.models.draw_ticket import DrawTicket
from event.models.draw_prize import DrawPrize
from event.models.draw_event import DrawEvent
 
@shared_task
def auto_pick_expired_tickets():
    now = timezone.now()
    # Find tickets where the turn has started more than 5 minutes ago and are still unused.
    expired_tickets = DrawTicket.objects.filter(
        used=False,
        turn_started_at__lte=now - timedelta(minutes=5)
    )
    for ticket in expired_tickets:
        event = ticket.event
        # Check that prizes are available for the event.
        available_prizes = DrawPrize.objects.filter(event=event, ticket__isnull=True)
        if not available_prizes.exists():
            continue  # Skip if no prizes remain.
        # Call the stored procedure to assign a prize.
        with connection.cursor() as cursor:
            cursor.callproc("sp_draw_prize_for_tickets", [ticket.id])
            result = cursor.fetchone()
        if result:
            # Mark the ticket as used and update the event.
            ticket.used = True
            ticket.save()
            event.remaining_prizes = max(0, event.remaining_prizes - 1)
            event.save()
