from django.shortcuts import render
from django.http import HttpResponse
from daily_focus.forms import FocusForm, FocusImageForm
from craft.utils import ConnectSqlite


def home(request):
    return render(request, 'daily_focus/home.html')


def upload_focus(request):
    if request.method == 'POST':
        pass
        return HttpResponse('post')
    else:
        focus_form = FocusForm()
        focus_image_form = FocusImageForm()
        return render(request, 'daily_focus/upload_focus.html',
                      {
                        'focus_form': focus_form,
                        'focus_image_form': focus_image_form,
                      }
                      )

