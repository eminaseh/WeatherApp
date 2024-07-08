import requests
from django.shortcuts import render, redirect
from .forms import LokacijaForma
from .utility.timestamp import vratiSateIMiute
from .models import Grad, Korisnik
from .forms import GradForma, KreirajKorisnikaForma, KorisnikForma
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group


# Create your views here.
@login_required(login_url='prijava')
@allowed_users(allowed_roles=['admin','korisnik'])
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=hr&appid=33e1b16ca67cd2ceba55e49dad09aab9'
    forecastUrl = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&lang=hr&appid=33e1b16ca67cd2ceba55e49dad09aab9'

    grad = request.user.korisnik.grad_naziv

    if request.method=='POST':
        form = LokacijaForma(request.POST)
        if(form.is_valid()):
            grad = form.cleaned_data['grad']

    r = requests.get(url.format(grad)).json()
    res = requests.get(forecastUrl.format(grad)).json()

    prognozaLista = res['list']
    izabranaPrognoza = [ ]
    for i in range (0,4):

        timestamp = prognozaLista[i]['dt']
        sati_i_minute = vratiSateIMiute(timestamp)

        grad_prognoza = {
            'tacno_vrijeme': sati_i_minute,
            'temp': prognozaLista[i]['main']['temp'],
            'opis': prognozaLista[i]['weather'][0]['description'],
            'ikona': prognozaLista[i]['weather'][0]['icon'],
        }
        izabranaPrognoza.append(grad_prognoza)

    izlazak = r['sys']['sunrise']
    zalazak = r['sys']['sunset']

    sati_izlazak = vratiSateIMiute(izlazak)
    sati_zalazak = vratiSateIMiute(zalazak)

    grad_vrijeme = {
        'grad': grad,
        'drzava': r['sys']['country'],
        'temperatura': r['main']['temp'],
        'opis': r['weather'][0]['description'],
        'ikona': r['weather'][0]['icon'],
        'osjeti_se': r['main']['feels_like'],
        'vjetar': r['wind']['speed'],
        'vlaznost_zraka': r['main']['humidity'],
        'izlazak_sunca': sati_izlazak,
        'zalazak_sunca': sati_zalazak,
        'najvisa_temperatura': r['main']['temp_max'],
        'najniza_temperatura': r['main']['temp_min'],
    }

    context = {'grad_vrijeme': grad_vrijeme,'grad': grad}
    context["form"] = LokacijaForma()
    context['izabranaPrognoza'] = izabranaPrognoza

    return render(request, 'vrijemeApp/vrijemeApp.html', context)


@login_required(login_url='prijava')
@allowed_users(allowed_roles=['admin','korisnik'])
def profil(request):
    korisnik = request.user.korisnik
    form = KorisnikForma(instance=korisnik)

    if request.method == 'POST':
        form = KorisnikForma(request.POST, request.FILES, instance=korisnik)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'vrijemeApp/user.html', context)



@login_required(login_url='prijava')
@allowed_users(allowed_roles=['admin','korisnik'])
def gradovi(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=hr&appid=33e1b16ca67cd2ceba55e49dad09aab9'

    greska_poruka = ''
    poruka = ''
    poruka_klasa = ''

    if request.method == 'POST':
        form = GradForma(request.POST)

        if form.is_valid():
            novi_grad = form.cleaned_data['naziv']
            postojeci_grad_broj = Grad.objects.filter(naziv=novi_grad).count()

            if postojeci_grad_broj == 0:
                r = requests.get(url.format(novi_grad)).json()

                if r['cod'] == 200:
                    form.save()

                else:
                    greska_poruka = 'Grad ne postoji.'
            else:
                greska_poruka = 'Grad već postoji u bazi podataka.'

        if greska_poruka:
            poruka = greska_poruka
            poruka_klasa = 'greska'

        else:
            poruka = 'Grad je uspješno dodan.'
            poruka_klasa = 'uspjeh'

    form = GradForma()

    gradovi = Grad.objects.all()

    vrijeme_podaci = []

    for grad in gradovi:
        r = requests.get(url.format(grad)).json()

        grad_vrijeme = {
            'grad': grad.naziv,
            'drzava': r['sys']['country'],
            'temperatura': r['main']['temp'],
            'opis': r['weather'][0]['description'],
            'ikona': r['weather'][0]['icon'],
        }

        vrijeme_podaci.append(grad_vrijeme)

    context = {'vrijeme_podaci': vrijeme_podaci, 'form': form, 'poruka': poruka, 'poruka_klasa': poruka_klasa}

    return render(request, 'vrijemeApp/gradovi.html', context)

@login_required(login_url='prijava')
@allowed_users(allowed_roles=['admin'])
def izbrisi_grad(request, grad_naziv):
    Grad.objects.get(naziv=grad_naziv).delete()
    return redirect('gradovi')


@unauthenticated_user
def registracija(request):
    form = KreirajKorisnikaForma()

    if request.method == 'POST':
        form = KreirajKorisnikaForma(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='korisnik')
            user.groups.add(group)

            Korisnik.objects.create(
                user=user,
            )

            messages.success(request, 'Uspješno kreiran korisnički račun ' + username)
            return redirect('prijava')

    context = {'form':form}
    return render(request, 'vrijemeApp/registracija.html', context)

@unauthenticated_user
def prijava(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'Korisničko ime ili lozinka su neispravni')


    context = {}
    return render(request, 'vrijemeApp/prijava.html', context)



def odjava(request):
    logout(request)
    return redirect('prijava')



