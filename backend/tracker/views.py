from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, date
from .models import Transaction


@login_required
def transaction_list(request):

    if request.method == 'POST':
        Transaction.objects.create(
            user=request.user,
            amount=float(request.POST.get('amount')),
            transaction_type=request.POST.get('transaction_type'),
            note=request.POST.get('note'),
            category=request.POST.get('category'),
            date=request.POST.get('date')
        )
        return redirect('/')

    delete_id = request.GET.get('delete')
    if delete_id:
        Transaction.objects.filter(id=delete_id, user=request.user).delete()
        return redirect('/')

    transactions = Transaction.objects.filter(user=request.user)

    total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
    total_expense = sum(t.amount for t in transactions if t.transaction_type == 'expense')
    balance = total_income - total_expense

    category_totals = {}
    for t in transactions:
        category_totals[t.category] = category_totals.get(t.category, 0) + t.amount

    # MongoDB-safe monthly summary
    monthly_summary = {}

    for t in transactions:
        key = t.date.strftime('%Y-%m')

        if key not in monthly_summary:
            monthly_summary[key] = {
                'income': 0,
                'expense': 0,
                'balance': 0
            }

        monthly_summary[key][t.transaction_type] += t.amount
        monthly_summary[key]['balance'] = (
            monthly_summary[key]['income']
            - monthly_summary[key]['expense']
    )

    return render(request, 'tracker/transactions.html', {
        'transactions': transactions,
        'total_incomes': total_income,
        'total_expenses': total_expense,
        'balance_amount': balance,
        'category_totals': category_totals,
        'monthly_summarys': monthly_summary
    })


@login_required
def edit_transaction(request, txn_id):
    txn = Transaction.objects.get(id=txn_id, user=request.user)

    if request.method == 'POST':
        txn.amount = float(request.POST.get('amount'))
        txn.transaction_type = request.POST.get('transaction_type')
        txn.note = request.POST.get('note')
        txn.date = request.POST.get('date')
        txn.category = request.POST.get('category')
        txn.save()
        return redirect('/')

    return render(request, 'tracker/edit.html', {'txn': txn})


@login_required
def monthly_summary(request):

    year_param = request.GET.get('year')

    if year_param and year_param.isdigit():
        selected_year = int(year_param)
    else:
        selected_year = datetime.now().year

    transactions = Transaction.objects.filter(
        user=request.user,
        date__year=selected_year
    )

    summary = []
    for m in range(1, 13):
        income = sum(
            t.amount for t in transactions
            if t.date.month == m and t.transaction_type == 'income'
        )
        expense = sum(
            t.amount for t in transactions
            if t.date.month == m and t.transaction_type == 'expense'
        )

        summary.append({
            'month': date(selected_year, m, 1),
            'm_income': income,
            'm_expense': expense,
            'balance': income - expense
        })

    years = sorted(
        set(t.date.year for t in Transaction.objects.filter(user=request.user))
    )

    return render(request, 'tracker/monthly_summary.html', {
        'summarys': summary,
        'years': years,
        'selected_year': selected_year
    })


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('/')
        messages.error(request, 'Invalid username or password')

    return render(request, 'tracker/login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')