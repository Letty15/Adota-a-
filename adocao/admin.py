from django.contrib import admin
from .models import Pet, SolicitacaoAdocao

admin.site.site_header = "Adota Aí · Painel de Administração"
admin.site.site_title = "Adota Aí Admin"
admin.site.index_title = "Bem-vindo(a) ao painel de gestão"


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
        "pet",
        "status",
        "data_solicitacao",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "usuario__username",
        "pet__nome",
    )
