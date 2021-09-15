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


class MessageSerializer(ModelSerializer):
    #ticket = TicketSerializer()
    #sender = ProfileSerializer()

    class Meta:
        model = Message
        fields = '__all__'
