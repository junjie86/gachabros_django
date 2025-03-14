from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wallet.models import Transaction

@login_required
def transaction_history(request):
    transactions_list = Transaction.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(transactions_list, 10)  # Show 10 transactions per page

    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)

    return render(request, 'wallet/transaction_history.html', {'transactions': transactions})
