from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.api.permissions import IsSupport
from core.api.serializers import TicketSerializer, TicketDetailSerializer
from core.api.services import create_message, put_profile_in_request
from core.models import Ticket


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    # lookup_field = 'slug'
    permission_classes = (IsAuthenticated,)

    action_to_serializer = {
        "list": TicketSerializer,
        "retrieve": TicketDetailSerializer,
        "update": TicketSerializer
    }
    permission_to_method = {
        "update": [IsSupport]
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )

    def get_permissions(self):
        return [permission() for permission in self.permission_to_method.get(
            self.action,
            self.permission_classes
        )]

    # show user tickets or all tickets for support
    def get_queryset(self, *args, **kwargs):
        profile = self.request.user.profile
        if profile.service_type == '2':
            return Ticket.objects.all()

        return Ticket.objects.filter(creator=profile)

    def update(self, request, *args, **kwargs):
        put_profile_in_request(request)
        return super().update(request)

    def create(self, request, *args, **kwargs):
        put_profile_in_request(request)
        return super().create(request)

    # action for post messages in ticket
    @action(methods=['post'], detail=True)
    def post_message(self, request, pk=None):
        create_message(request, pk)
        return Response(status=status.HTTP_201_CREATED)
