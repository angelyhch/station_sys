from django.shortcuts import render
from django.http import HttpResponse
from daily_focus.forms import FocusForm, FocusImageForm
from craft.utils import ConnectSqlite


def home(request):
    return render(request, 'daily_focus/home.html')


def upload_focus(request):
    if request.method == 'POST':
        focus_form = FocusForm(request.POST)
        focus_image_form = FocusImageForm(request.FILES)

        if focus_form.is_valid() and focus_image_form.is_valid():
            new_focus_form = focus_form.save(commit=False)
            new_focus_image_form = focus_image_form.save(commit=False)

            new_focus_form.user = request.user
            new_focus_image_form.focus = new_focus_form

            new_focus_form.save()
            new_focus_image_form.save()

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

