from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import CadastroUsuarioForm
from .models import Perfil
from adocao.models import Pet

def home(request):

    pets = Pet.objects.filter(disponivel=True)[:4]

    return render(
        request,
        'home.html',
        {'pets': pets}
    )

def cadastro_usuario(request):

    if request.method == "POST":

        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():

            usuario = form.save()

            Perfil.objects.create(usuario=usuario)

            messages.success(
                request,
                "Cadastro realizado com sucesso! Faça login para continuar."
            )

            return redirect("login")

        else:
            messages.error(
                request,
                "Verifique os dados informados."
            )

    else:

        form = CadastroUsuarioForm()

    return render(
        request,
        "usuarios/cadastro.html",
        {
            "form": form
        }
    )


@login_required
def perfil(request):

    return render(
        request,
        'usuarios/perfil.html'
    )


def logout_usuario(request):

    logout(request)

    messages.info(
        request,
        "Você saiu da sua conta."
    )

    return redirect("login")


def adocao_responsavel(request):

    return render(
        request,
        "adocao_responsavel.html"
    )