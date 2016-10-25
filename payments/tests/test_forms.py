from django.test import TestCase

from payments.forms import PaymentForm
from payments.models import Account


class PaymentFormTest(TestCase):
    def setUp(self):
        Account.objects.create(first_name="Harry", last_name="Potter", email="harry.potter@test.com")
        Account.objects.create(first_name="Hermione", last_name="Granger", email="hermione.granger@test.com")

    def test_valid_form(self):
        form_data = {'origin_account': 1, 'dest_account': 2, 'amount': 20}
        form = PaymentForm(form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_balance_exceeded(self):
        form_data = {'origin_account': 1, 'dest_account': 2, 'amount': 2000}
        form = PaymentForm(form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_same_destination_acct(self):
        form_data = {'origin_account': 1, 'dest_account': 1, 'amount': 10}
        form = PaymentForm(form_data)
        self.assertFalse(form.is_valid())
