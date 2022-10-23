from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import *
# Create your views here.


class VistaRegistrarse(View):

    def get(self, request):
        formulario = UserCreationFormExtended()
        return render(request, "signup/signup.html", {'formulario': formulario})

    def post(self, request):
        formulario = UserCreationFormExtended(request.POST)

        if formulario.is_valid():
            usuario = formulario.save()

            messages.success(request, "Se a registrado correctamente")
            login(request, usuario)

            return redirect('inicio')

        messages.error(request, "No se ha registrado, revisar datos")

        return render(request, 'signup/signup.html', {'formulario': formulario})


def salir(request):
    logout(request)
    return redirect('login')


def entrar(request):
    if request.method == "POST":
        formulario = AuthenticationForm(request, data=request.POST)

        if formulario.is_valid():
            nom_user = formulario.cleaned_data.get("username")
            pas_user = formulario.cleaned_data.get("password")

            usuario = authenticate(username=nom_user, password=pas_user)

            if usuario is not None:
                login(request, usuario)
                redireccion = request.GET.get('next', '/')

                return redirect(redireccion)
            else:
                messages.error(request, "Esta cuenta esta inactiva")
        else:
            messages.error(request, "Usuario o contraseña incorrecta")

    formulario = AuthenticationForm()

    return render(request, "login/login.html", {'formulario': formulario})


def error_404(request, exception):
    messages.warning(request, "La página solicitada no se encuentra")
    return redirect('inicio')


def error_500(request, exception=None):
    messages.info(request, " El servidor encontró una condición inesperada que le impide completar la petición")
    return redirect('inicio')


def error_403(request, exception=None):
    messages.info(request, "El servidor ha recibido la petición, pero rechaza enviar una respuesta")
    return redirect('inicio')


def error_400(request, exception=None):
    messages.info(request, "El servidor no puede procesar la petición debido a un error del cliente")
    return redirect('inicio')
