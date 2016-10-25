from django import forms

from .models import Account


class PaymentForm(forms.Form):
    origin_account = forms.ChoiceField(choices=[])
    dest_account = forms.ChoiceField(choices=[])
    amount = forms.DecimalField(label='Amount(£)',max_digits=10)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        account_list = [(x.pk, x.get_account_holder()) for x in Account.objects.all()]
        self.fields['origin_account'].choices = account_list
        self.fields['dest_account'].choices = account_list

    def clean(self):
        """
        Perform business logic validation
        1) Check that both to and from accounts exist
        2) Check that to and from accounts are not the same
        3) Check that the transfer amount is less than the from account balance
        4) Check that the transfer amount is a positive number

        :return:
        """
        form_data = self.cleaned_data

        origin_account = Account.objects.get(pk=form_data['origin_account'])
        dest_account = Account.objects.get(pk=form_data['dest_account'])

        if not origin_account:
            raise forms.ValidationError('The account you selected does not exist')
        if not dest_account:
            raise forms.ValidationError('The account you selected does not exist')
        if origin_account.account_number == dest_account.account_number:
            raise forms.ValidationError('Your recipient account must be different from the sender account')
        if form_data['amount'] <= 0:
            raise forms.ValidationError('You must enter a positive number.')
        if origin_account.balance < form_data['amount']:
            raise forms.ValidationError('Your transaction was not successful. You have requested to transfer an amount '
                                        'greater than the account balance.')
