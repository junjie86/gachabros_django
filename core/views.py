from django.http import JsonResponse

def status(request):
    return JsonResponse({'status': 'Django with Supabase is running!'})
