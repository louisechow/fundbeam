from datetime import datetime

from django.db import models


class Account(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    account_number = models.AutoField(primary_key=True)
    account_type = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=200.00)

    def __str__(self):
        return "First name; {}, Last name: {}, Email: {}, " \
               "Account number: {}, Account type: {}, Balance: {}".format(self.first_name, self.last_name, self.email,
                                                                          self.account_number,self.account_type,
                                                                          self.balance)


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_date = models.DateTimeField(default=datetime.now)
    origin_account = models.ForeignKey(Account, related_name='origin_account', null=True)
    destination_account = models.ForeignKey(Account, related_name='destination_account', null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_type = models.CharField(max_length=1, null=True)

    def __str__(self):
        return "Transaction Id: {}, Transaction date: {}, " \
               "Origin account: {}, Destination account: {}, " \
               "Amount: {}, Transaction Type: {}".format(
            self.id, self.transaction_date,
            self.origin_account, self.destination_account,
            self.amount, self.transaction_type
        )
