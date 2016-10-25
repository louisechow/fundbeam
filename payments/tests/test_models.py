from decimal import Decimal
from django.test import TestCase

from payments.models import Account


class AccountTestCase(TestCase):
    def setUp(self):
        Account.objects.create(first_name="Harry", last_name="Potter", email="harry.potter@test.com")

    def test_credit_account_success(self):
        test_amount = Decimal(50)
        account = Account.objects.get(first_name="Harry")
        account.credit_balance(test_amount)
        self.assertEqual(account.balance, 250.00)

    def test_debit_account_success(self):
        test_amount = Decimal(50)
        account = Account.objects.get(first_name="Harry")
        account.debit_balance(test_amount)
        self.assertEqual(account.balance, 150.00)

    def test_debit_account_fail(self):
        test_amount = Decimal(500)
        account = Account.objects.get(first_name="Harry")
        with self.assertRaises(ValueError) as context:
            account.debit_balance(test_amount)

        self.assertEqual('The debit amount is greater than the balance.', str(context.exception))

    def test_get_account_holder(self):
        account = Account.objects.get(first_name="Harry")
        self.assertEqual(account.get_account_holder(), 'Harry Potter')
