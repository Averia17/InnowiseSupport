from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Ticket, Message, Profile


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class ProfileSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketDetailSerializer(ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = '__all__'

    def get_messages(self, obj):
        messages = Message.objects.select_related('sender').filter(ticket__pk=obj.pk)
        serialized_messages = MessageSerializer(messages, many=True).data
        return serialized_messages


class MessageSerializer(ModelSerializer):
    #ticket = TicketSerializer()
    #sender = ProfileSerializer()

    class Meta:
        model = Message
        fields = '__all__'
