from django.db import models
from django.urls import reverse
from django.utils import timezone
from user.models import User
from landlord.models import Property
import datetime

# Create your models here.

class Application(models.Model):
    tenant          = models.ForeignKey(User, on_delete=models.CASCADE)
    move_in_date    = models.DateField(default=datetime.date.today)
    bio             = models.TextField()
    
    dorm            = models.ForeignKey(Property, on_delete=models.CASCADE)
    is_approved     = models.BooleanField(default=False)
    is_disapproved  = models.BooleanField(default=False)

    schedule        = models.DateField(default=datetime.date.today)

    created_at      = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.tenant.username

    def get_absolute_url(self):
        return reverse("tenant:tenant")

    def approve(self):
        self.is_approved = True
        self.save()

    def disapprove(self):
        self.is_disapproved = True
        self.save()

class MessageRoom(models.Model):
    name        = models.CharField(max_length=30, default='defaultRoom')
    dorm        = models.OneToOneField(Property, on_delete=models.CASCADE, null=True, blank=True)
    members     = models.ManyToManyField(User, related_name='members', verbose_name='members of this room')
    created_at  = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    

class Message(models.Model):
    room        = models.ForeignKey(MessageRoom, on_delete=models.CASCADE, null=True)
    author      = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content     = models.TextField()
    created_at  = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author.username

    def last_messages(this_room):
        message_room = MessageRoom.objects.filter(name=this_room)[0]
        messages = Message.objects.filter(room=message_room).order_by('-created_at')[:10]
        return reversed(messages)
    