from django import forms
from django.core.exceptions import ValidationError

from .models import Account, Transaction

class PaymentForm(forms.Form):
    accounts = (
        ('1', 'Louise Chow'),
        ('2', 'Harry Potter'),
        ('3', 'Hermione Granger'),
        ('4', 'Ron Weasley'),
    )

    origin_account = forms.ChoiceField(choices=accounts)
    dest_account = forms.ChoiceField(choices=accounts)
    amount = forms.DecimalField(label='Amount', max_digits=10)

    def clean(self):
        form_data = self.cleaned_data

        origin_account = Account.objects.get(pk=form_data['origin_account'])
        if not origin_account:
            raise forms.ValidationError('The account you selected does not exist')

        dest_account = Account.objects.get(pk=form_data['dest_account'])
        if not dest_account:
            raise forms.ValidationError('The account you selected does not exist')

        print('#######')
        print(origin_account.balance)
        print(form_data['amount'])

        if origin_account.balance < form_data['amount']:
            raise forms.ValidationError('Your transaction was not successful. You have requested to transfer an amount greater than the account balance.')
