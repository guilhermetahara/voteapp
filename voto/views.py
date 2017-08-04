from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . import models
from django.forms.formsets import formset_factory
from django.views import View
from django.views.generic.edit import FormView


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

    form_class = models.VotacaoForm
    formset_class = formset_factory(models.EscolhaForm)

    def get(self, request, username):
        form = self.form_class(None)
        formset = self.formset_class(None)
        return render(request, 'userindex.html', {'form': form, 'formset': formset})

    def post(self, request, username):

        votacao_obj = request.POST['pergunta']
        usuario = request.user

        #cria entrada da votação no banco de dados
        models.Votacao.objects.create(pergunta=votacao_obj, autor=usuario)

        #Procura pela votação criada
        #Conta quantas escolhas foram criadas pelo POST e cria entradas no banco de dados
        ultima_votação = models.Votacao.objects.latest('id')
        num_escolhas = 0
        totalforms = 'form-TOTAL_FORMS'
        for totalforms in request.POST:
            num_escolhas = num_escolhas + 1
        num_escolhas = (num_escolhas-1)/2
        for i in range(0, int(num_escolhas)-1):
            escolha_obj = request.POST['form-' + str(i) + '-escolha']
            models.Escolha.objects.create(votacao=ultima_votação, escolha=escolha_obj)
        return redirect('/usuario/' + str(request.user.username) + '/votacao/' + str(votacao_obj) + '/')


class Votacao(View):

    def get(self, request, username):
        url = str(request.path)
        pergunta = url.rsplit('/', 2)[1]
        user = models.User.objects.filter(username=username)
        votacao = models.Votacao.objects.filter(autor=user, pergunta=pergunta)
        escolhas = models.Escolha.objects.filter(votacao=votacao)
        data_dic = {}
        lista_escolhas = []

        for v in votacao:
            data_dic['pergunta'] = (v.pergunta)
        for e in escolhas:
           lista_escolhas.append(e)
        print(lista_escolhas)
        data_dic['lista_escolhas'] = lista_escolhas
        return render(request, 'Votacao.html', data_dic)

    def post(self, request, username):
        print(request.POST['escolha_id'])
        url = str(request.path)
        pergunta = url.rsplit('/', 2)[1]
        autor = models.User.objects.get(username=username)
        votacao = models.Votacao.objects.get(pergunta=pergunta, autor=autor)
        id = request.POST['escolha_id']
        print(id)
        escolha = models.Escolha.objects.get(id=id)
        models.Voto.objects.create(votacao=votacao, escolha=escolha)
        return redirect('/')
