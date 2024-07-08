from django import forms
from django.forms import ModelForm, TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Grad, Korisnik


class GradForma(ModelForm):
    class Meta:
        model = Grad
        fields = ['naziv']
        widgets = {'naziv': TextInput(attrs={'class': 'pretrazivanje'})}

class LokacijaForma(forms.Form):
       grad = forms.CharField(max_length=35)


class KreirajKorisnikaForma(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {'username': TextInput(attrs={'class': 'forma-login-input'}),
                   'email': TextInput(attrs={'class': 'forma-login-input'}),

                   }

class KorisnikForma(ModelForm):
    class Meta:
        model = Korisnik
        fields = '__all__'
        exclude = ['user']
        widgets = {'ime': TextInput(attrs={'class': 'forma-login-input'}),
                   'email': TextInput(attrs={'class': 'forma-login-input'}),
                   'grad_naziv': TextInput(attrs={'class': 'forma-login-input'}),
                   }



