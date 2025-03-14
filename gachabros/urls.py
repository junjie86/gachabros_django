# myproject/urls.py

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login'), name='root_redirect'),
    path('', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('wallet/', include('wallet.urls')),
    path('event/', include('event.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)