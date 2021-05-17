from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
import uuid
import time
import os

# Create your models here.

'''
tuple(zip(range(len(line_list)), line_list))
'''
line_list = apps.get_app_config('daily_focus').LINE_LIST
line_station_dict = apps.get_app_config('daily_focus').LINE_STATION_DICT

line_list_choices = tuple(zip(line_list, line_list))


class Focus(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='focus')
    line = models.CharField(verbose_name='线体', choices=line_list_choices, max_length=300)
    station = models.CharField(verbose_name='工位', max_length=300,blank=True)
    focus_content = models.TextField(verbose_name='关注内容', blank=True)
    focus_start = models.DateField(verbose_name='关注开始')
    focus_end = models.DateField(verbose_name='关注结束')
    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-focus_end']

    def __str__(self):
        return f'created[{self.created}] + focus_end[{self.focus_end}]'


def user_directory_path(instance, filename):
    ext = filename.split('.', 1)[-1]
    station = instance.focus.station
    line = instance.focus.line
    filename = f'{time.strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:10]}.{ext}'
    return os.path.join('images/daily_focus/', line, station,  filename)


class FocusImage(models.Model):
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    focus = models.ForeignKey(Focus, on_delete=models.PROTECT, related_name='images')

