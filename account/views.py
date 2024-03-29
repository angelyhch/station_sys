from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user:
                login(request, user)
                return HttpResponse('Welcome, 你已成功登陆。')
            else:
                return HttpResponse('Sorry, 你的账户名或者密码有错误。')
        else:
            return HttpResponse('输入错误。')
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'account/login.html', {'form':login_form})