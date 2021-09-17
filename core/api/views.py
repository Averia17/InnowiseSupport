from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.api.permissions import IsSupport
from core.api.serializers import TicketSerializer, TicketDetailSerializer, ProfileSerializer, UserSerializer
from core.models import Ticket, Message


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    # lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)

    action_to_serializer = {
        "list": TicketSerializer,
        "retrieve": TicketDetailSerializer,
        "update": TicketSerializer
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )

    def get_permissions(self):
        if self.request.method == 'PUT':
            permission_classes = [IsSupport]
            return [permission() for permission in permission_classes]
        return super().get_permissions()

    # show user tickets or all tickets for support
    def get_queryset(self, *args, **kwargs):
        profile = self.request.user.profile
        if profile.service_type == '2':
            return Ticket.objects.all()

        return Ticket.objects.filter(creator=profile)

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['creator'] = request.user.profile.pk
        request.data._mutable = False
        return super().create(request)

    # action for post messages in ticket
    @action(methods=['post'], detail=True)
    def post_message(self, request, pk=None):
        Message.objects.create(sender=request.user.profile,
                               ticket=Ticket.objects.get(pk=pk),
                               text=request.data.get('text'))
        return Response(status=status.HTTP_201_CREATED)


# class UserViewSet(mixins.CreateModelMixin):
#     serializer_class = UserSerializer
#     def create(self, request, *args, **kwargs):
#         user =