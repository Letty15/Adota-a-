from django.urls import path
from . import views

urlpatterns = [
    path(
        'formulario/',
        views.formulario_adocao,
        name='formulario'
    ),
    path('quiz/', views.quiz, name='quiz'),
    path('parceiros/', views.parceiros, name='parceiros'),

    path(
        'pets/',
        views.lista_pets,
        name='lista_pets'
    ),
    path(
        'pets/<int:pk>/',
        views.detalhe_pet,
        name='detalhe_pet'
    ),
]
