import os
import time
import uuid

from django.apps import apps
from django.contrib.auth.models import User
from django.db import models

from PIL import Image
from io import BytesIO
from django.core.files import File

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
    station = models.ForeignKey(Station, verbose_name='工位', on_delete=models.SET_NULL, null=True,
                                related_name='focuses')

    class Meta:
        ordering = ['-focus_end']

    def __str__(self):
        return f'created[{self.created}] + focus_end[{self.focus_end}]'


def user_directory_path(instance, filename):
    ext = filename.split('.', 1)[-1]
    station = instance.focus.station.name
    line = instance.focus.station.line.name
    filename = f'{time.strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:10]}.{ext}'
    return os.path.join('images/daily_focus/', line, station, filename)


def user_directory_path2(instance, filename):
    ext = filename.split('.', 1)[-1]
    station = instance.focus.station.name
    line = instance.focus.station.line.name
    filename = f'{time.strftime("%Y%m%d%H%M%S")}{uuid.uuid4().hex[:10]}.{ext}'
    return os.path.join('images_thumbnail/daily_focus/', line, station, filename)


def create_thumbnail(instance):
    instance.image_thumbnail.delete()
    img = Image.open(instance.image.file)
    img.thumbnail((200, 200))
    img_byte = BytesIO()
    img_ext = 'jpeg'
    img.save(img_byte, img_ext)
    instance.image_thumbnail.save(instance.image.name, File(img_byte), save=False)
    instance.last_image = instance.image.name


class FocusImage(models.Model):
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    image_thumbnail = models.ImageField(upload_to=user_directory_path2, blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    focus = models.ForeignKey(Focus, on_delete=models.SET_NULL, null=True, related_name='images')

    def __init__(self, *args, **kwargs):
        super(FocusImage, self).__init__(*args, **kwargs)
        self.last_image = self.image.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        '''
        重写save函数，每次保存时，自动保存thumbnail缩略图
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        '''

        if self.image.name != self.last_image:  #如果image有变化，才进行缩略图更新。
            create_thumbnail(self)

        super().save()


class FocusAfterImage(models.Model):
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    image_thumbnail = models.ImageField(upload_to=user_directory_path2, blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    focus = models.ForeignKey(Focus, on_delete=models.SET_NULL, null=True, related_name='after_images')

    def __init__(self, *args, **kwargs):
        super(FocusAfterImage, self).__init__(*args, **kwargs)
        self.last_image = self.image.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        '''
        重写save函数，每次保存时，自动保存thumbnail缩略图
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        '''
        if self.image.name != self.last_image:  #如果image有变化，才进行缩略图更新。
            create_thumbnail(self)

        super().save()
