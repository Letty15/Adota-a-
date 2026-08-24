from django.urls import path
from django.contrib.auth.views import LoginView

from . import views
from .forms import LoginForm

urlpatterns = [

    # Página inicial
    path(
        '',
        views.home,
        name='home'
    ),

    # Login
    path(
        'login/',
        LoginView.as_view(
            template_name='usuarios/login.html',
            authentication_form=LoginForm
        ),
        name='login'
    ),

    # Cadastro
    path(
        'cadastro/',
        views.cadastro_usuario,
        name='cadastro'
    ),

    # Perfil
    path(
        'perfil/',
        views.perfil,
        name='perfil'
    ),

    path(
    'adocao-responsavel/',
    views.adocao_responsavel,
    name='adocao_responsavel'
),

    # Logout
    path(
        'logout/',
        views.logout_usuario,
        name='logout'
    ),

]