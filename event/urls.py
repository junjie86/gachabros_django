from django.urls import path
from event.views.ticket_views import ticket_history
from event.views.event_views import event_history
from event.views.draw_event_views import draw_event_view, pick_prize, buy_ticket, auto_pick_prize

urlpatterns = [
    path('ticketlist/', ticket_history, name='ticket_history'),
    path('eventlist/', event_history, name='event_history'),
    path("event/<int:event_id>/", draw_event_view, name="draw_event"),
    path("event/<int:event_id>/pick/<int:prize_id>/", pick_prize, name="pick_prize"),
    path("event/<int:event_id>/buy-ticket/", buy_ticket, name="buy_ticket"),
    path('event/<int:event_id>/auto-pick/', auto_pick_prize, name='auto_pick_prize'),
]
print("URL patterns registered:", urlpatterns)