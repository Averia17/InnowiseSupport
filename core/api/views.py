from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.api.serializers import TicketSerializer, MessageSerializer
from core.models import Ticket, Message


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    # lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)
    queryset = Ticket.objects.all()

    def retrieve(self, request, *args, **kwargs):
        if Ticket.objects.get(pk=kwargs['pk']).creator != request.user.profile \
                and request.user.profile.service_type != '2':
            return Response({'response': 'You dont have permission to the ticket'}, status=status.HTTP_403_FORBIDDEN)

        queryset = Message.objects.select_related('sender').filter(ticket__pk=kwargs['pk'])
        serializer = MessageSerializer(queryset, many=True)
        return Response({'messages': serializer.data})

    # support must see all tickets
    def list(self, request, *args, **kwargs):
        profile = request.user.profile
        if profile.service_type == '2':
            queryset = Ticket.objects.all()
            serializer = TicketSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = Ticket.objects.filter(creator=profile)
            serializer = TicketSerializer(queryset, many=True)
            return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.user.profile.service_type != '2':
            return Response({'response': 'You dont have permission to the put request'},
                            status=status.HTTP_403_FORBIDDEN)
        Ticket.objects.filter(pk=kwargs['pk']).update(service_type=request.data.get('service_type'))

        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def post_message(self, request, pk=None):
        text = request.data.get('text')
        sender = request.user.profile
        ticket = Ticket.objects.get(pk=pk)
        Message.objects.create(sender=sender, ticket=ticket, text=text)
        return Response(status=status.HTTP_201_CREATED)

    # def create(self, request, *args, **kwargs):
    #     post_data = request.data
    #     print(post_data)
    #     ticket = Ticket.objects.create(service_type='1', title=post_data.get('title'))
    #     ticket.save()
    #     Message.objects.create(sender=request.user.auth_token, text=post_data.get('text'), ticket=ticket)
    #     serializer = TicketSerializer()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
