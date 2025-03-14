from django.urls import path
from core.views.registration_views import register
from core.views.auth_views import user_login
from core.views.dashboard_views import dashboard

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),
    path('dashboard/', dashboard, name='dashboard'),
]
