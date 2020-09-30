from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',)
    token = models.CharField(verbose_name='токен', max_length=32, blank=False, unique=True, null=False)