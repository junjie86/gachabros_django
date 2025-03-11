# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from . import views  # Import views from the project directory

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello_world, name='hello_world'),
    path('api/', include('core.urls')),
]