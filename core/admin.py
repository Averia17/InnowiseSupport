from django.contrib import admin

# Register your models here.
from core.models import Profile, Ticket, Message

admin.site.register(Profile)
admin.site.register(Ticket)
admin.site.register(Message)
