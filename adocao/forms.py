from django import forms
from .models import SolicitacaoAdocao


class SolicitacaoAdocaoForm(forms.ModelForm):

    class Meta:
        model = SolicitacaoAdocao

        exclude = [
            'usuario',
            'status',
            'data_solicitacao'
        ]

        widgets = {

            'nome_pet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do pet que deseja adotar'
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