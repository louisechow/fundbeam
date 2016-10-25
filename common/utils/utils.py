from django.core.mail import send_mail
from payments.models import Transaction



def do_transaction(instances_to_save):
    for inst in instances_to_save:
        inst.save()