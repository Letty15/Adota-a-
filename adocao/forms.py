from django import forms
from .models import SolicitacaoAdocao, Pet


class SolicitacaoAdocaoForm(forms.ModelForm):

    class Meta:
        model = SolicitacaoAdocao

        exclude = [
            'usuario',
            'status',
            'data_solicitacao'
        ]

        widgets = {

            'pet': forms.Select(attrs={
                'class': 'form-select'
            }),

            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Conte por que você deseja adotar este pet...'
            }),

            'tem_criancas': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[
                (True, 'Sim'),
                (False, 'Não')
            ]),

            'tem_outros_pets': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[
                (True, 'Sim'),
                (False, 'Não')
            ]),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Só mostra pets que ainda estão disponíveis para adoção
        self.fields['pet'].queryset = Pet.objects.filter(disponivel=True)
        self.fields['pet'].empty_label = "Selecione um pet"


class PetFiltroForm(forms.Form):
    """Filtros da lista de pets: um campo por eixo, todos opcionais."""

    EIXOS = [
        "especie",
        "porte",
        "energia",
        "temperamento",
        "independencia",
        "tolerancia_barulho",
        "experiencia",
        "cuidados",
    ]
    CONVIVE = ["convive_criancas", "convive_outros_pets"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        select = {'class': 'form-select form-select-sm'}

        for nome in self.EIXOS:
            campo = Pet._meta.get_field(nome)
            self.fields[nome] = forms.ChoiceField(
                label=str(campo.verbose_name).capitalize(),
                required=False,
                choices=[('', 'Qualquer')] + list(campo.choices),
                widget=forms.Select(attrs=select),
            )

        for nome in self.CONVIVE:
            campo = Pet._meta.get_field(nome)
            self.fields[nome] = forms.ChoiceField(
                label=str(campo.verbose_name).capitalize(),
                required=False,
                choices=[('', 'Qualquer'), ('sim', 'Sim')],
                widget=forms.Select(attrs=select),
            )


class PetForm(forms.ModelForm):
    """Cadastro e edição de pets (usado nas páginas de administrador)."""

    AJUDA = {
        'especie': 'Define a espécie que o quiz vai recomendar.',
        'porte': 'Tamanho do animal já adulto.',
        'energia': 'Calmo: prefere descansar. Agitado: precisa de muita brincadeira e passeio.',
        'temperamento': 'Arisco: reservado, leva tempo para confiar. Dócil: busca carinho e colo.',
        'independencia': 'Dependente: sofre ficando sozinho. Independente: fica bem sozinho por várias horas.',
        'tolerancia_barulho': 'Sensível: se assusta fácil. Tranquilo: lida bem com barulho e movimento.',
        'experiencia': 'O quanto a pessoa precisa saber de pets para cuidar bem dele.',
        'cuidados': 'Medicação, tratamento contínuo, escovação frequente, necessidades especiais.',
        'convive_criancas': 'Se "Não", ele nunca aparece no quiz para quem tem crianças em casa.',
        'convive_outros_pets': 'Se "Não", ele nunca aparece no quiz para quem já tem outros pets.',
    }

    class Meta:
        model = Pet
        fields = [
            'nome', 'idade', 'descricao', 'foto',
            'especie', 'porte', 'energia', 'temperamento', 'independencia',
            'tolerancia_barulho', 'experiencia', 'cuidados',
            'convive_criancas', 'convive_outros_pets',
            'disponivel',
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'foto': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for nome, campo in self.fields.items():
            widget = campo.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, forms.Select):
                widget.attrs['class'] = 'form-select'
            else:
                widget.attrs['class'] = 'form-control'

            if nome in self.AJUDA:
                campo.help_text = self.AJUDA[nome]

        self.fields['idade'].widget.attrs['placeholder'] = 'Ex.: 2 anos, 8 meses'
        self.fields['descricao'].widget.attrs['placeholder'] = (
            'Conte a história e a personalidade do pet...'
        )
        # Selects obrigatórios começam em branco, para não passar sem escolher
        for nome in self.AJUDA:
            campo = self.fields[nome]
            campo.choices = [('', 'Selecione...')] + [
                c for c in campo.choices if c[0] != ''
            ]

