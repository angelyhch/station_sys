from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Focus(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='focus')
    station = models.CharField(max_length=300)
    line = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)


class FocusImage(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    focus = models.ForeignKey(Focus, on_delete=models.PROTECT, related_name='images')

