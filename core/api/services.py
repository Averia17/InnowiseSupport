from core.models import Ticket, Message
from core.tasks import send_mail_task


def create_message(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    sender = request.user.profile

    Message.objects.create(sender=sender,
                           ticket=ticket,
                           text=request.data.get('text'))
    send_mail_task.delay(ticket.pk, sender.pk)


def put_profile_in_request(request):
    request.POST._mutable = True
    request.data['creator'] = request.user.profile.pk
    request.POST._mutable = False
