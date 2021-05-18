from django.shortcuts import render
from django.http import HttpResponse
from daily_focus.forms import FocusForm, FocusImageForm
from craft.utils import ConnectSqlite, logger
from daily_focus.models import Focus, FocusImage
from django.apps import apps
import datetime


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


def delete_focus_image(request):
    pass



def focus_detail(request, focus_id=47):

    focus = Focus.objects.get(id=focus_id)
    images = list(focus.images.all())
    focus_form = FocusForm(focus.__dict__)
    line_station_dict = apps.get_app_config('daily_focus').LINE_STATION_DICT

    if request.method == 'POST':
        post_form = FocusForm(request.POST)
        post_data = post_form.cleaned_data
        for key in post_data.keys():
            focus.__setattr__(key, post_data[key])
        focus.save()

        recv_images = request.FILES.getlist('images')
        if len(recv_images) > 0:
            for image in recv_images:
                new_foucs_image = FocusImageForm().save(commit=False)
                new_foucs_image.focus = focus
                new_foucs_image.image = image
                new_foucs_image.save()

        return HttpResponse('update success')

    else:
        return render(request, 'daily_focus/focus_detail.html',
                      {
                          'focus': focus,
                          'images': images,
                          'focus_form': focus_form,
                          'line_station_dict': line_station_dict,
                      }
                      )


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
        logger.info(recv_data)
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

