from django.urls import path
from core.views.registration_views import register
from core.views.auth_views import user_login

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
]
