from django.contrib.auth.models import User
from django.db import models

class Messages(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='resiver', on_delete=models.CASCADE)
    message_text = models.TextField(verbose_name='Message')
    date_time = models.DateTimeField(verbose_name='date time when message was send', auto_now_add=True)
