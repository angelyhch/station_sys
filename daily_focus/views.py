from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'daily_focus/home.html')
