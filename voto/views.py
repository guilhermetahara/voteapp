from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . import models
from django.forms.formsets import formset_factory
from django.views import View


def createuser(request):

    if request.method == 'GET':
        form = models.UserForm
        return render(request, 'userform.html', {'form': form})

    elif request.method == 'POST':
        form = models.UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('/')
        else:
            return render(request, 'userform.html', {'form': form})


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')


def userlogin(request):

    form = models.LoginForm
    if request.method == 'GET':
        return render(request, 'login.html', {'form': form})

    if request.method == 'POST':
        form = models.LoginForm(request.POST)
        usuario = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=usuario, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'form': form})

def userlogout(request):
    if request.method == 'GET':
        logout(request)
        return redirect('/')

class Userindex(View):

    def get(self, request):
        return render(request, 'userindex.html', )


class Poll(View):

    def get(self, request):
        retur
