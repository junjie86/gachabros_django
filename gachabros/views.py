# myproject/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from supabase import create_client
import json, os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        response = supabase.auth.sign_up(email=email, password=password)
        if response.user:
            return JsonResponse({'message': 'Signup successful'}, status=201)
        return JsonResponse({'error': response.error.message}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=405)
 
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        response = supabase.auth.sign_in(email=email, password=password)
        if response.session:
            return JsonResponse({'token': response.session.access_token}, status=200)
        return JsonResponse({'error': response.error.message}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=405)
  
  
def protected(request):
    if request.user:
        return JsonResponse({'message': 'Authenticated', 'user': request.user})
    return JsonResponse({'error': 'Unauthorized'}, status=401)
  
def hello_world(request):
    response_data = {
        'message': 'Hello, World!',
        'method': request.method,
        'headers': dict(request.headers),
    }
    return JsonResponse(response_data)