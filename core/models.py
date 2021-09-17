from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    STATUS_TYPES = [
        ('1', 'User'),
        ('2', 'Support'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    service_type = models.CharField(choices=STATUS_TYPES, default='1', max_length=1)

    def __str__(self):
        return self.user.username


class Ticket(models.Model):
    STATUS_TYPES = [
        ('1', 'Unsolved'),
        ('2', 'Solved'),
        ('3', 'Frozen'),
    ]
    service_type = models.CharField(choices=STATUS_TYPES, default='1', max_length=1)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=63, null=True, blank=True)

    def __str__(self):
        return f'{self.pk} {self.service_type}'


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.sender.user.username}: {self.text}'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
