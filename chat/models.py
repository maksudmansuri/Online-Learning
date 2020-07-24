from django.db import models
from accounts.models import CustomUser
# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models

User = CustomUser

class Message(models.Model):
    user = models.ForeignKey(CustomUser, related_name='user_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def last_10_messages():
        return Message.objects.order_by('created_at').all()[:10]