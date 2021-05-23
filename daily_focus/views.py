from django.shortcuts import render
from django.http import HttpResponse
from daily_focus.forms import FocusForm, StationForm, FocusImageForm
from craft.utils import ConnectSqlite, logger
from daily_focus.models import Focus, FocusImage, FocusAfterImage
from django.apps import apps
import datetime
import time
import urllib
import os
from django.conf import settings
import json
def home(request):
    return render(request, 'daily_focus/home.html')

def focus_today(request):
    todays = Focus.objects.filter(focus_end__gt=datetime.date.today()).order_by("focus_end")
    focus_form = FocusForm()
    line_station_dict = apps.get_app_config('daily_focus').LINE_STATION_DICT

    return render(request, 'daily_focus/focus_today.html',
                  {
                      'todays': todays,
                      'focus_form': focus_form,
                      'line_station_dict': line_station_dict,
                      'datetime': datetime,
                  }
                  )


def focus_record(request, focus_id=1):
    focus = Focus.objects.get(id=focus_id)

    focus_days = []
    start = focus.focus_start
    end = focus.focus_end
    while start <= end:
        focus_days.append(start)
        start += datetime.timedelta(days=1)

    return render(request, 'daily_focus/focus_record.html',
                  {
                      'focus': focus,
                      'focus_days': focus_days,
                  }
                  )


def delete_focus_image(request):
    logger.debug(request.POST)
    image_src_url = request.POST['image_src']
    image_path1 = urllib.parse.unquote(image_src_url)
    image_field = image_path1[7:]   #把路径中/media/给去掉

    image = FocusImage.objects.get(image=image_field)
    image_id = image.id

    image.delete()

    return HttpResponse(f'success delete image{image_id}')


def delete_focus_after_image(request):
    logger.debug(request.POST)
    image_src_url = request.POST['after_image_src']
    image_path1 = urllib.parse.unquote(image_src_url)
    image_field = image_path1[7:]   #把路径中/media/给去掉

    image = FocusAfterImage.objects.get(image=image_field)
    image_id = image.id
    image.delete()

    return HttpResponse(f'success delete image-{image_id}')


def focus_detail(request, focus_id=1):
    focus = Focus.objects.get(id=focus_id)
    focus_form = FocusForm(focus.__dict__)
    line_station_dict = apps.get_app_config('daily_focus').LINE_STATION_DICT

    if request.method == 'POST':
        post_form = FocusForm(request.POST)

        if post_form.is_valid():
            logger.debug(post_form.cleaned_data)
            post_data = post_form.cleaned_data
        else:
            return HttpResponse('输入数据不全，请补全数据再提交！')

        for key in post_data.keys():
            focus.__setattr__(key, post_data[key])
        focus.save()

        return HttpResponse('关注数据更新成功')

    else:
        return render(request, 'daily_focus/focus_detail.html',
                      {
                          'focus': focus,
                          'focus_form': focus_form,
                          'line_station_dict': line_station_dict,
                      }
                      )


def upload_image(request):
    if request.method == 'POST':
        recv_data = request.POST
        focus_id = recv_data['focus_id']
        focus = Focus.objects.get(id=focus_id)

        recv_images = request.FILES.getlist('images')
        if len(recv_images) > 0:
            for image in recv_images:
                new_focus_image = FocusImage()
                new_focus_image.focus = focus
                new_focus_image.image = image
                new_focus_image.save()

        recv_after_images = request.FILES.getlist('after_images')
        if len(recv_after_images) > 0:
            for image in recv_after_images:
                new_focus_after_image = FocusAfterImage()
                new_focus_after_image.focus = focus
                new_focus_after_image.image = image
                new_focus_after_image.save()

        return HttpResponse('success upload image!')


def focus_list(request):
    all_focus = Focus.objects.all()

    return render(request, 'daily_focus/focus_list.html',
                  {
                      'all_focus': all_focus,
                  }
                  )


def upload_focus(request):
    line_station_dict = apps.get_app_config('daily_focus').LINE_STATION_DICT
    if request.method == 'POST':
        recv_data = request.POST
        logger.debug(recv_data)
        focus_form = FocusForm(request.POST)
        if focus_form.is_valid():
            new_focus = focus_form.save(commit=False)
            new_focus.user = request.user
            new_focus.save()

        recv_images = request.FILES.getlist('images')
        if len(recv_images) > 0:
            for image in recv_images:
                new_foucs_image = FocusImageForm().save(commit=False)
                new_foucs_image.focus = new_focus
                new_foucs_image.image = image
                new_foucs_image.save()

        return HttpResponse('success')

    else:
        focus_form = FocusForm()
        return render(request, 'daily_focus/upload_focus.html',
                      {
                        'focus_form': focus_form,
                        'line_station_dict': line_station_dict,
                      }
                      )

def record_add_focus(request):
    '''
    记录表格自动加入focus
    :param request:
    :return:
    '''

    recv_data = request.POST

    focus = FocusForm(recv_data).save(commit=False)
    focus.user = request.user

    focus.save()

    return HttpResponse('添加成功，请移步【今日关注】查看！')
