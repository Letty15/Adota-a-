from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import CadastroUsuarioForm
from .models import Perfil
from adocao.models import Pet, SolicitacaoAdocao

def home(request):

    pets = Pet.objects.filter(disponivel=True)[:4]
    total_acolhidos = Pet.objects.count()
    total_adocoes = SolicitacaoAdocao.objects.filter(status='Aprovado').count()

    return render(
        request,
        'home.html',
        {
            'pets': pets,
            'total_acolhidos': total_acolhidos,
            'total_adocoes': total_adocoes,
        }
    )

def cadastro_usuario(request):

    if request.method == "POST":

        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():

            try:
                with transaction.atomic():
                    usuario = form.save()
                    Perfil.objects.create(usuario=usuario)
            except IntegrityError:
                # Duas requisições simultâneas (ex.: clique duplo no botão)
                # ou nome de usuário criado no meio tempo.
                form.add_error("username", "Este nome de usuário já está em uso.")
            else:
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

    solicitacoes = (
        SolicitacaoAdocao.objects
        .filter(usuario=request.user)
        .select_related('pet')
        .order_by('-data_solicitacao')
    )

    return render(
        request,
        'usuarios/perfil.html',
        {'solicitacoes': solicitacoes}
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