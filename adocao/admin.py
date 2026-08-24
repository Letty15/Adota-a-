from django.contrib import admin
from .models import Pet, SolicitacaoAdocao


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "idade",
        "porte",
        "disponivel",
    )

    list_filter = (
        "porte",
        "disponivel",
    )

    search_fields = (
        "nome",
    )


@admin.register(SolicitacaoAdocao)
class SolicitacaoAdocaoAdmin(admin.ModelAdmin):

    list_display = (
        "usuario",
        "nome_pet",
        "status",
        "data_solicitacao",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "usuario__username",
        "nome_pet",
    )