from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from . import matching
from .forms import SolicitacaoAdocaoForm, PetFiltroForm, PetForm
from .models import Pet


def staff_required(view):
    """Só administradores (is_staff). Visitante vai para o login;
    usuário comum volta para a home com um aviso."""

    @wraps(view)
    @login_required
    def envelope(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Apenas administradores podem acessar esta página.")
            return redirect('home')
        return view(request, *args, **kwargs)

    return envelope


@login_required
def formulario_adocao(request):
    if request.method == 'POST':
        form = SolicitacaoAdocaoForm(request.POST)

        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.usuario = request.user
            solicitacao.save()

            messages.success(
                request,
                "Sua solicitação foi enviada com sucesso! Aguarde a análise da equipe."
            )

            return redirect('perfil')

    else:
        # Vindo da página do pet (?pet=ID), já deixa o pet selecionado
        pet_id = request.GET.get('pet')
        initial = {'pet': pet_id} if pet_id and pet_id.isdigit() else {}
        form = SolicitacaoAdocaoForm(initial=initial)

    return render(
        request,
        'adocao/formulario.html',
        {'form': form}
    )


def quiz(request):
    return render(request, 'quiz.html')


# Campos que o quiz envia na URL (média das respostas, de 1 a 3)
CAMPOS_PERFIL = [
    'energia', 'porte', 'temperamento', 'independencia',
    'tolerancia_barulho', 'experiencia', 'cuidados',
]


def _numero_1_a_3(valor):
    try:
        return min(3.0, max(1.0, float(valor)))
    except (TypeError, ValueError):
        return None


def _votos(valor):
    try:
        return min(100, max(0, int(valor)))
    except (TypeError, ValueError):
        return 0


def quiz_resultado(request):
    """Recebe o perfil montado pelo quiz (via URL) e mostra os 3 melhores pets."""

    perfil = {}
    for campo in CAMPOS_PERFIL:
        numero = _numero_1_a_3(request.GET.get(campo))
        if numero is not None:
            perfil[campo] = numero

    if not perfil:
        # Acessou direto, sem responder o quiz
        return redirect('quiz')

    votos_especie = {
        'cao': _votos(request.GET.get('v_cao')),
        'gato': _votos(request.GET.get('v_gato')),
        'outro': _votos(request.GET.get('v_outro')),
    }
    tem_criancas = request.GET.get('criancas') == '1'
    tem_outros_pets = request.GET.get('outros_pets') == '1'

    pets = list(Pet.objects.filter(disponivel=True))
    dados = [
        {
            'obj': pet,
            'nome': pet.nome,
            'especie': pet.especie,
            'porte': pet.porte,
            'energia': pet.energia,
            'temperamento': pet.temperamento,
            'independencia': pet.independencia,
            'tolerancia_barulho': pet.tolerancia_barulho,
            'experiencia': pet.experiencia,
            'cuidados': pet.cuidados,
            'convive_criancas': pet.convive_criancas,
            'convive_outros_pets': pet.convive_outros_pets,
        }
        for pet in pets
    ]

    melhores = matching.ranking(
        dados, perfil, votos_especie,
        tem_criancas=tem_criancas,
        tem_outros_pets=tem_outros_pets,
        limite=3,
    )

    nomes_especie = dict(Pet.ESPECIE)
    recomendadas = [
        nomes_especie[e] for e in matching.especie_recomendada(votos_especie)
    ]

    return render(request, 'adocao/quiz_resultado.html', {
        'melhores': melhores,
        'especies_recomendadas': recomendadas,
        'tem_criancas': tem_criancas,
        'tem_outros_pets': tem_outros_pets,
        'total_disponiveis': len(pets),
    })


def parceiros(request):
    return render(request, 'parceiros.html')


def lista_pets(request):
    # Administradores podem ver também os pets já adotados (?todos=1)
    mostrar_todos = request.user.is_staff and request.GET.get('todos') == '1'
    pets = Pet.objects.all() if mostrar_todos else Pet.objects.filter(disponivel=True)

    filtro = PetFiltroForm(request.GET)
    filtros_ativos = False

    if filtro.is_valid():
        for campo, valor in filtro.cleaned_data.items():
            if valor:
                pets = pets.filter(**{campo: valor})
                filtros_ativos = True

    return render(
        request,
        'adocao/lista_pets.html',
        {
            'pets': pets,
            'filtro': filtro,
            'filtros_ativos': filtros_ativos,
            'mostrar_todos': mostrar_todos,
        }
    )


def detalhe_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    return render(
        request,
        'adocao/detalhe_pet.html',
        {'pet': pet}
    )


# ----- Gestão de pets (somente administradores) -----

@staff_required
def pet_criar(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save()
            messages.success(request, f"{pet.nome} foi cadastrado com sucesso!")
            return redirect('detalhe_pet', pk=pet.pk)
    else:
        form = PetForm(initial={'disponivel': True})

    return render(request, 'adocao/pet_form.html', {
        'form': form,
        'titulo': 'Cadastrar novo pet',
        'pet': None,
    })


@staff_required
def pet_editar(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, f"Os dados de {pet.nome} foram atualizados.")
            return redirect('detalhe_pet', pk=pet.pk)
    else:
        form = PetForm(instance=pet)

    return render(request, 'adocao/pet_form.html', {
        'form': form,
        'titulo': f'Editar {pet.nome}',
        'pet': pet,
    })


@staff_required
@require_POST
def pet_excluir(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    nome = pet.nome
    pet.delete()
    messages.success(request, f"{nome} foi removido.")
    return redirect('lista_pets')
