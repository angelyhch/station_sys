from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
import uuid
import time
import os
from sorl import thumbnail

import datetime
import django
# Create your models here.

'''
tuple(zip(range(len(line_list)), line_list))
'''
line_list = apps.get_app_config('daily_focus').LINE_LIST
line_station_dict = apps.get_app_config('daily_focus').LINE_STATION_DICT

line_list_choices = tuple(zip(line_list, line_list))


class ClassGroup(models.Model):
    name = models.CharField(verbose_name='班组名', max_length=300)

    def __str__(self):
        return self.name


class Line(models.Model):
    name = models.CharField(verbose_name='线体名', max_length=300)
    class_name = models.ForeignKey(ClassGroup, on_delete=models.SET_NULL, null=True, related_name='lines')

    def __str__(self):
        return self.name


    # chexing = models.ManyToManyField
#
#
# class CheXing(models.Model):
#     name = models.CharField(verbose_name='车型名', max_length=300)
#     code = models.CharField(verbose_name='车型代码', max_length=300)


class Station(models.Model):
    name = models.CharField(verbose_name='工位编号', max_length=300)
    mingcheng = models.CharField(verbose_name='工位名称', max_length=300)
    line = models.ForeignKey(Line, verbose_name='线体', on_delete=models.SET_NULL, null=True, related_name='stations')

    def __str__(self):
        return self.name


class Focus(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='focuses')
    focus_content = models.TextField(verbose_name='关注内容', blank=True)
    focus_start = models.DateField(verbose_name='关注开始')
    focus_end = models.DateField(verbose_name='关注结束')
    last_modify = models.DateTimeField(auto_now=True, db_index=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    station = models.ForeignKey(Station, verbose_name='工位', on_delete=models.SET_NULL, null=True, related_name='focuses')

    class Meta:
        ordering = ['-focus_end']

    def __str__(self):
        return f'created[{self.created}] + focus_end[{self.focus_end}]'


def user_directory_path(instance, filename):
    ext = filename.split('.', 1)[-1]
    station = instance.focus.station.name
    line = instance.focus.station.line.name
    name = f'{time.strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:10]}.{ext}'
    return os.path.join('images/daily_focus/', line, station,  name)


def user_directory_path_thumbnail(instance, filename):
    ext = filename.split('.', 1)[-1]
    station = instance.focus.station.name
    line = instance.focus.station.line.name
    name = f'{time.strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:10]}.{ext}'
    return os.path.join('images_thumbnail/daily_focus/', line, station,  name)


class FocusImage(models.Model):
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    focus = models.ForeignKey(Focus, on_delete=models.SET_NULL, null=True, related_name='images')
    # image_thumbnail = models.ImageField(upload_to=user_directory_path_thumbnail, blank=True)

    # def save(self, *args, **kwargs):



class FocusAfterImage(models.Model):
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    focus = models.ForeignKey(Focus, on_delete=models.SET_NULL, null=True, related_name='after_images')
