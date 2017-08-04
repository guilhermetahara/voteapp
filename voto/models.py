from django.db import models
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    conf_password = forms.CharField(label='Confirme sua senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        labels = {
            'firs_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Usuario',
            'email': 'E-mail',
            'password': 'Senha'
        }
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('conf_password')

        if password1 != password2:
            msg = "Senha não bate"
            self.add_error('password_confirm', msg)
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=150)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        return cleaned_data

class Votacao(models.Model):
    pergunta = models.CharField(max_length=1000)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def contagem_escolhas(self):
        return self.escolha_set.count()

    def total_votos(self):
        total = 0

        for escolha in self.escolha_set.all():
            total = total + escolha.contagem_voto()
        return total


    def __str__(self):
        return self.pergunta

class VotacaoForm(forms.ModelForm):
    class Meta:
        model = Votacao
        fields = ['pergunta']

class Escolha(models.Model):
    escolha = models.CharField(max_length=500)
    votacao = models.ForeignKey(Votacao)

    def contagem_voto(self):
        return self.voto_set.count()

    def __str__(self):
        return self.escolha

class EscolhaForm(forms.ModelForm):
    class Meta:
        model = Escolha
        fields = ['escolha']

class Voto(models.Model):

    escolha = models.ForeignKey(Escolha)
    votacao = models.ForeignKey(Votacao)

    def __unicode__(self):
        return u'Voto em %s' % (self.choice)