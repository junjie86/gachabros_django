from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from event.models import DrawEvent

@login_required
def event_history(request):
    event_list = DrawEvent.objects.order_by('-start_time')  # Use a valid field

    paginator = Paginator(event_list, 10)  # Show 10 events per page
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    return render(request, 'event/event_history.html', {'events': events})
