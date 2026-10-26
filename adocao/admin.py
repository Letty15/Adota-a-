from django.contrib import admin, messages
from .models import Pet, SolicitacaoAdocao

admin.site.site_header = "Adota Aí · Painel de Administração"
admin.site.site_title = "Adota Aí Admin"
admin.site.index_title = "Bem-vindo(a) ao painel de gestão"


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "especie",
        "idade",
        "porte",
        "energia",
        "temperamento",
        "disponivel",
    )

    list_filter = (
        "disponivel",
        "especie",
        "porte",
        "energia",
        "temperamento",
        "independencia",
        "tolerancia_barulho",
        "experiencia",
        "cuidados",
        "convive_criancas",
        "convive_outros_pets",
    )

    search_fields = (
        "nome",
    )

    fieldsets = (
        ("Informações básicas", {
            "fields": ("nome", "idade", "descricao", "foto", "disponivel"),
        }),
        ("Características para o match (todas obrigatórias)", {
            "description": (
                "Estes campos alimentam os filtros da lista de pets e o quiz de "
                "compatibilidade. Escolha com cuidado: é com eles que o sistema "
                "sugere o pet certo para cada pessoa."
            ),
            "fields": (
                "especie",
                "porte",
                "energia",
                "temperamento",
                "independencia",
                "tolerancia_barulho",
                "experiencia",
                "cuidados",
                "convive_criancas",
                "convive_outros_pets",
            ),
        }),
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

    actions = ["aprovar_solicitacoes", "recusar_solicitacoes"]

    def _mudar_status(self, request, queryset, status):
        # save() de cada objeto (e não queryset.update) para o pet
        # ser marcado como indisponível ao aprovar.
        for solicitacao in queryset:
            solicitacao.status = status
            solicitacao.save()
        self.message_user(
            request,
            f"{queryset.count()} solicitação(ões) marcada(s) como {status}.",
            messages.SUCCESS,
        )

    @admin.action(description="Aprovar solicitações selecionadas")
    def aprovar_solicitacoes(self, request, queryset):
        self._mudar_status(request, queryset, "Aprovado")

    @admin.action(description="Recusar solicitações selecionadas")
    def recusar_solicitacoes(self, request, queryset):
        self._mudar_status(request, queryset, "Recusado")
