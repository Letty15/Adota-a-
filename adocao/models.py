from django.db import models
from django.contrib.auth.models import User


class SolicitacaoAdocao(models.Model):

    STATUS = [
        ("Pendente", "Pendente"),
        ("Aprovado", "Aprovado"),
        ("Recusado", "Recusado"),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    pet = models.ForeignKey(
        'Pet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solicitacoes'
    )

    motivo = models.TextField()

    tem_criancas = models.BooleanField()

    tem_outros_pets = models.BooleanField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pendente"
    )

    data_solicitacao = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        nome = self.pet.nome if self.pet else "Pet removido"
        return f"{self.usuario.username} - {nome}"


class Pet(models.Model):

    nome = models.CharField(max_length=100)

    idade = models.CharField(max_length=50)

    porte = models.CharField(max_length=30)

    descricao = models.TextField()

    foto = models.ImageField(
        upload_to="pets/"
    )

    disponivel = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.nome