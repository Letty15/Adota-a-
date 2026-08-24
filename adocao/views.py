from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SolicitacaoAdocaoForm


@login_required
def formulario_adocao(request):
    if request.method == 'POST':
        form = SolicitacaoAdocaoForm(request.POST)

        if form.is_valid():
            from django.contrib import messages

            solicitacao = form.save(commit=False)
            solicitacao.usuario = request.user
            solicitacao.save()

            messages.success(
                request,
                "Sua solicitação foi enviada com sucesso! Aguarde a análise da equipe."
            )

            return redirect('perfil')

    else:
        form = SolicitacaoAdocaoForm()

    return render(
        request,
        'adocao/formulario.html',
        {'form': form}
    )


def quiz(request):
    return render(request, 'quiz.html')
    
def parceiros(request):
    return render(request, 'parceiros.html')