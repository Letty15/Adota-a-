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