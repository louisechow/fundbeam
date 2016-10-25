from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.contrib import messages

from common.utils import utils

from .models import Account, Transaction
from .forms import PaymentForm


def account_list(request):
    accounts = Account.objects.all()
    return render(request, 'payments/account_list.html', {'accounts': accounts})


def account_transactions(request):
    account_number = None
    if request.method == 'GET':
        account_number = request.GET['account_number']
    user = Account.objects.get(pk=account_number)
    transactions = Transaction.objects.filter(
        Q(origin_account__account_number=user.account_number) |
        Q(destination_account__account_number = user.account_number)).order_by('-transaction_date')

    transaction_template = 'payments/transactions.html'
    data = {'transactions': transactions}

    return render_to_response(transaction_template, data)


def make_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data

            transaction_step_list = []

            origin_account = Account.objects.get(pk=form_data['origin_account'])
            origin_account.balance = origin_account.balance - form_data['amount']
            transaction_step_list.append(origin_account)

            dest_account = Account.objects.get(pk=form_data['dest_account'])
            dest_account.balance = dest_account.balance + form_data['amount']
            transaction_step_list.append(dest_account)

            new_transaction = Transaction(origin_account=origin_account,
                                          destination_account=dest_account, amount=form_data['amount'],
                                          transaction_type='C')
            transaction_step_list.append(new_transaction)

            with transaction.atomic():
                utils.do_transaction(transaction_step_list)

            send_notifications(new_transaction, origin_account.email, dest_account.email)

            messages.add_message(request, messages.INFO, 'Your transfer was successful')
            return HttpResponseRedirect('/')
    else:
        form = PaymentForm

    return render(request, 'payments/pay.html', {'form':form})


def send_notifications(transaction_details, sender_email, recipient_email):
    mail_msg = '{} has been successfully transferred from account {} to account {}'.format(
        transaction_details.amount,
        transaction_details.origin_account.account_number,
        transaction_details.destination_account.account_number
    )

    send_mail('Your transfer was successful!', mail_msg, 'fundbeam@test.com', [sender_email, recipient_email],
              fail_silently=False)
