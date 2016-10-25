from django.core import mail
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse

from payments.models import Account, Transaction
from payments.views import send_notifications


class ViewTests(TestCase):
    def setUp(self):
        Account.objects.create(first_name="Harry", last_name="Potter", email="harry.potter@test.com")
        Account.objects.create(first_name="Hermione", last_name="Granger", email="hermione.granger@test.com")

        from_account = Account.objects.get(pk=1)
        to_account = Account.objects.get(pk=2)
        Transaction.objects.create(origin_account=from_account,destination_account=to_account, amount=10)

    def test_account_list_view(self):
        """
        Test that we are returning all accounts
        :return:
        """
        response = self.client.get(reverse('account_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['accounts']), 2)

    def test_account_transactions_view_sender(self):
        """
        Test that a transaction shows up under the senders transaction list
        :return:
        """
        response = self.client.get(reverse('account_transactions'), {'account_number': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transactions']), 1)

    def test_account_transactions_view_recipient(self):
        """
        Test that a transaction shows up under the recipients transaction list
        :return:
        """
        response = self.client.get(reverse('account_transactions'), {'account_number': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['transactions']), 1)

    def test_make_payment(self):
        """
        Test that a transaction is successfully made
        :return:
        """
        transactions = Transaction.objects.all()
        self.assertEqual(len(transactions), 1)

        response = self.client.post(reverse('pay'), {'origin_account': 1, 'dest_account': 2, 'amount': 10})
        self.assertEqual(response.status_code, 302)

        transactions = Transaction.objects.all()
        self.assertEqual(len(transactions), 2)

        self.assertEqual(len(mail.outbox), 1)

    def test_send_email(self):
        """
        Test that we are successfully sending an email
        :return:
        """
        transaction = Transaction.objects.get(pk=1)
        test_sender_email = 'test1@test.com'
        test_recipient_email = 'test2@test.com'

        send_notifications(transaction, test_sender_email, test_recipient_email)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [test_sender_email, test_recipient_email])
        self.assertEquals(mail.outbox[0].subject, 'Your transfer was successful!')