from django.urls import path
from . import views

urlpatterns = [
    path(
        'formulario/',
        views.formulario_adocao,
        name='formulario'
    ),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/resultado/', views.quiz_resultado, name='quiz_resultado'),
    path('parceiros/', views.parceiros, name='parceiros'),

    path(
        'pets/',
        views.lista_pets,
        name='lista_pets'
    ),
    path('pets/novo/', views.pet_criar, name='pet_criar'),
    path('pets/<int:pk>/editar/', views.pet_editar, name='pet_editar'),
    path('pets/<int:pk>/excluir/', views.pet_excluir, name='pet_excluir'),
    path(
        'pets/<int:pk>/',
        views.detalhe_pet,
        name='detalhe_pet'
    ),
]
