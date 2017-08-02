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

class poll(models.Model):
    poll_id = models.AutoField(primary_key=True)
    poll = models.CharField(max_length=400)
    created_by = models.CharField(max_length=400, default='')

    def __str__(self):
        return self.poll

class pollForm(forms.ModelForm):
    class Meta:
        model = poll
        fields = ['poll', 'created_by']
        widgets = {'author': forms.HiddenInput()}