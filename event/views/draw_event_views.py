from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.db import DatabaseError, connection
from datetime import timedelta

from event.models.draw_event import DrawEvent
from event.models.draw_ticket import DrawTicket
from event.models.draw_prize import DrawPrize

def pick_prize(request, event_id, prize_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")
    
    event = get_object_or_404(DrawEvent, pk=event_id)
    prize = get_object_or_404(DrawPrize, pk=prize_id, event=event, ticket__isnull=True)
    
    # Get the current active ticket.
    current_ticket = DrawTicket.objects.filter(event=event, used=False).order_by("purchased_at").first()
    if not current_ticket or current_ticket.user != request.user.profile:
        return JsonResponse({"error": "Not your turn"}, status=400)
    
    # Ensure the ticket is still within its 5-minute window.
    if not current_ticket.turn_started_at:
        # If turn hasn't started yet, start it now
        current_ticket.turn_started_at = timezone.now()
        current_ticket.save()
    
    expiration_time = current_ticket.turn_started_at + timedelta(minutes=5)
    if timezone.now() > expiration_time:
        return JsonResponse({"error": "Time expired"}, status=400)
    
    try:
        # Call the stored procedure to draw a prize.
        with connection.cursor() as cursor:
            cursor.callproc("sp_draw_prize_for_tickets", [current_ticket.id])
            result = cursor.fetchone()  # Fetch the prize details.
        
        if not result:
            return JsonResponse({"error": "Failed to draw prize"}, status=500)
        
        # Parse the prize details from the stored procedure.
        prize_name, prize_description, prize_rarity = result
        
        # Return the prize details to the frontend.
        return JsonResponse({
            "message": "Prize picked",
            "prize": {
                "name": prize_name,
                "description": prize_description,
                "rarity": prize_rarity
            }
        })
    
    except DatabaseError as e:
        # Catch database errors (e.g., no available prizes, invalid ticket).
        error_message = str(e).split("CONTEXT")[0].strip()
        return JsonResponse({"error": error_message}, status=400)
      
def draw_event_view(request, event_id):
    event = get_object_or_404(DrawEvent, pk=event_id)
    
    # If no prizes remain, event is over.
    if event.remaining_prizes <= 0:
        return render(request, "event_over.html", {"event": event})
    
    # Get tickets for this event in FIFO order.
    tickets = DrawTicket.objects.filter(event=event).order_by("purchased_at")
    current_ticket = tickets.filter(used=False).first()
    
    # Instead of auto-picking immediately when expired,
    # we let the client-side timer manage the expiration.
    ticket_expired = False
    if current_ticket and current_ticket.turn_started_at:
        expiration_time = current_ticket.turn_started_at + timedelta(minutes=5)
        # Removed immediate auto-pick logic.
        # We rely on the client-side timer to trigger auto-pick after 5 minutes.
        ticket_expired = False

    # Check if it is the current user's turn.
    user_profile = request.user.profile
    user_is_turn = bool(current_ticket and current_ticket.user == user_profile)
    
    # If it's the user's turn and the turn hasn't been started, start it now.
    if user_is_turn and current_ticket and not current_ticket.turn_started_at:
        current_ticket.turn_started_at = timezone.now()
        current_ticket.save()
    
    # Reset the timer for all active tickets of the user.
    if user_is_turn:
        DrawTicket.objects.filter(event=event, used=False, user=user_profile).update(turn_started_at=current_ticket.turn_started_at)
    
    # Retrieve the unopened prizes.
    unopened_prizes = DrawPrize.objects.filter(event=event, ticket__isnull=True)
    
    context = {
        "event": event,
        "current_ticket": current_ticket,
        "user_is_turn": user_is_turn,
        "ticket_expired": ticket_expired,
        "unopened_prizes": unopened_prizes,
        "queue": tickets,
        "event_id": event_id,  # For use in JavaScript.
    }
    return render(request, "event/draw_event.html", context)

def buy_ticket(request, event_id):
    event = get_object_or_404(DrawEvent, pk=event_id)
    
    # Only allow ticket purchase if the event is active.
    if event.status != "pending":
        return HttpResponseBadRequest("Ticket purchase not allowed for this event.")
    
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", 1))
            for _ in range(quantity):
                with connection.cursor() as cursor:
                    cursor.callproc("sp_purchase_event_ticket", [event.id, request.user.profile.id])
                    # Assuming the stored procedure returns a success message:
                    cursor.fetchone()
            
            # After purchasing, if it's the user's turn, reset the timer for all active tickets.
            current_ticket = DrawTicket.objects.filter(event=event, used=False).order_by("purchased_at").first()
            if current_ticket and current_ticket.user == request.user.profile:
                now = timezone.now()
                DrawTicket.objects.filter(event=event, used=False, user=request.user.profile).update(turn_started_at=now)
            
            return redirect("draw_event", event_id=event.id)
        
        except (DatabaseError, ValueError) as e:
            error_message = str(e).split("CONTEXT")[0].strip()
            return render(request, "event/buy_ticket.html", {
                "event": event,
                "error": error_message
            })
    
    return render(request, "event/buy_ticket.html", {"event": event})

def auto_pick_prize(request, event_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")
    
    try:
        event = get_object_or_404(DrawEvent, pk=event_id)
        
        # Get the current active ticket.
        current_ticket = DrawTicket.objects.filter(event=event, used=False).order_by("purchased_at").first()
        if not current_ticket:
            return JsonResponse({"error": "No active ticket found"}, status=400)
        
        # Ensure the timer has expired for the active turn.
        if not current_ticket.turn_started_at or timezone.now() <= (current_ticket.turn_started_at + timedelta(minutes=5)):
            return JsonResponse({"error": "Timer has not expired yet."}, status=400)
        
        # Get all active (unused) tickets for the current user.
        active_user = current_ticket.user
        active_tickets = DrawTicket.objects.filter(event=event, used=False, user=active_user).order_by("purchased_at")
        prizes_assigned = []
        
        for ticket in active_tickets:
            with connection.cursor() as cursor:
                # Call the stored procedure to draw a prize for the ticket.
                cursor.callproc("sp_draw_prize_for_tickets", [ticket.id])
                result = cursor.fetchone()
            
            if not result:
                continue  # Skip this ticket if no prize details were returned.
            
            # Parse the prize details from the stored procedure.
            prize_name, prize_description, prize_rarity = result
            
            # Mark the ticket as used.
            ticket.used = True
            ticket.save()
            
            # Optionally, update the event's remaining prizes count.
            if event.remaining_prizes > 0:
                event.remaining_prizes -= 1
                event.save()
            
            prizes_assigned.append({
                "ticket_id": ticket.id,
                "prize": {
                    "name": prize_name,
                    "description": prize_description,
                    "rarity": prize_rarity
                }
            })
        
        # If there are no remaining prizes, mark the event as completed.
        if event.remaining_prizes == 0:
            event.status = "completed"
            event.save()
        
        if not prizes_assigned:
            return JsonResponse({"error": "Failed to auto-pick any prizes."}, status=500)
        
        return JsonResponse({
            "message": "Auto-picked prizes for active tickets.",
            "prizes": prizes_assigned
        })
    
    except Exception as e:
        import logging
        logging.error(f"Auto-pick error: {str(e)}")
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)