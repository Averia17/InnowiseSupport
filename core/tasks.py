from celery import app
from django.conf import settings
from django.core.mail import send_mail

from core.models import Ticket, Profile


@app.shared_task
def send_mail_task(ticket_pk, sender_pk):
    ticket = Ticket.objects.get(pk=ticket_pk)
    sender = Profile.objects.get(pk=sender_pk)

    if sender.service_type == '2':
        send_mail(
            'Ticket ' + str(ticket.pk),
            'You received a response from support',
            settings.EMAIL_HOST_USER,
            [ticket.creator.user.email, ],
        )
