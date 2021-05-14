from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
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
    station = models.CharField(verbose_name='工位', max_length=300)
    focus_content = models.TextField(verbose_name='关注内容', blank=True)
    focus_start = models.DateField(verbose_name='关注开始')
    focus_end = models.DateField(verbose_name='关注结束')
    created = models.DateField(auto_now_add=True, db_index=True)


class FocusImage(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    focus = models.ForeignKey(Focus, on_delete=models.PROTECT, related_name='images')

