from django.utils import timezone

from django.db import models


class Account(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    account_number = models.AutoField(primary_key=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=200.00)

    def __str__(self):
        return "First name; {}, Last name: {}, Email: {}, " \
               "Account number: {}, Balance: {}".format(self.first_name, self.last_name, self.email,
                                                                          self.account_number, self.balance)
    def debit_balance(self, amount):
        if amount < self.balance:
            self.balance -= amount
        else:
            raise ValueError('The debit amount is greater than the balance.')

    def credit_balance(self, amount):
        self.balance += amount

    def get_account_holder(self):
        return "{} {}".format(self.first_name, self.last_name)


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_date = models.DateTimeField(default=timezone.now)
    origin_account = models.ForeignKey(Account, related_name='origin_account', null=True)
    destination_account = models.ForeignKey(Account, related_name='destination_account', null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return "Transaction Id: {}, Transaction date: {}, " \
               "Origin account: {}, Destination account: {}, " \
               "Amount: {}".format( self.id, self.transaction_date, self.origin_account, self.destination_account,
                                    self.amount)
