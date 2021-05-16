from django.shortcuts import render
from django.http import HttpResponse
from daily_focus.forms import FocusForm, FocusImageForm
from craft.utils import ConnectSqlite, logger
from daily_focus.models import Focus, FocusImage


def home(request):
    return render(request, 'daily_focus/home.html')


def focus_detail(request, focus_id=47):
    pass
    focus = Focus.objects.get(id=focus_id)
    images = list(focus.images.all())

    return render(request, 'daily_focus/focus_detail.html',
                  {
                      'focus': focus,
                      'images': images,
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
    if request.method == 'POST':
        recv_data = request.POST
        logger.info(recv_data)
        focus_form = FocusForm(request.POST)
        if focus_form.is_valid():
            new_focus = focus_form.save(commit=False)
            new_focus .user = request.user
            new_focus .save()

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
                      }
                      )

