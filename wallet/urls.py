from django.urls import path
from wallet.views.transaction_views import transaction_history

urlpatterns = [
    path('transactions/', transaction_history, name='transaction_history'),
]
