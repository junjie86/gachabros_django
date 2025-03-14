from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from event.models import DrawTicket
from core.models.profile import Profile  # Ensure correct user linking

@login_required
def ticket_history(request):
    try:
        profile = request.user.profile  # Ensure Profile exists for the user
        drawticket_list = DrawTicket.objects.filter(user=profile).order_by('-purchased_at')  # Use `purchased_at`
    except Profile.DoesNotExist:
        drawticket_list = DrawTicket.objects.none()  # Return empty queryset if no profile

    paginator = Paginator(drawticket_list, 10)  # Show 10 tickets per page
    page_number = request.GET.get('page')
    tickets = paginator.get_page(page_number)

    return render(request, 'event/ticket_history.html', {'tickets': tickets})
