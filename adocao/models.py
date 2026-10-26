from django.db import models
from django.contrib.auth.models import User

from . import choices


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

    def save(self, *args, **kwargs):
        status_anterior = None
        if self.pk:
            status_anterior = (
                SolicitacaoAdocao.objects
                .filter(pk=self.pk)
                .values_list("status", flat=True)
                .first()
            )

        super().save(*args, **kwargs)

        # Aprovar tira o pet da lista de disponíveis; desfazer a aprovação devolve.
        if self.pet:
            if self.status == "Aprovado" and self.pet.disponivel:
                self.pet.disponivel = False
                self.pet.save(update_fields=["disponivel"])
            elif status_anterior == "Aprovado" and self.status != "Aprovado":
                self.pet.disponivel = True
                self.pet.save(update_fields=["disponivel"])

    def __str__(self):
        nome = self.pet.nome if self.pet else "Pet removido"
        return f"{self.usuario.username} - {nome}"


class Pet(models.Model):

    # Listas usadas nos filtros e no quiz
    ESPECIE = choices.ESPECIE
    PORTE = choices.PORTE
    ENERGIA = choices.ENERGIA
    TEMPERAMENTO = choices.TEMPERAMENTO
    INDEPENDENCIA = choices.INDEPENDENCIA
    TOLERANCIA_BARULHO = choices.TOLERANCIA_BARULHO
    EXPERIENCIA = choices.EXPERIENCIA
    CUIDADOS = choices.CUIDADOS
    CONVIVE = choices.CONVIVE

    nome = models.CharField(max_length=100)

    idade = models.CharField(max_length=50)

    descricao = models.TextField()

    foto = models.ImageField(
        upload_to="pets/"
    )

    disponivel = models.BooleanField(
        default=True
    )

    # ----- Eixos de característica (todos obrigatórios) -----

    especie = models.CharField(
        "espécie", max_length=10, choices=choices.ESPECIE
    )

    porte = models.PositiveSmallIntegerField(
        "porte", choices=choices.PORTE
    )

    energia = models.PositiveSmallIntegerField(
        "nível de energia", choices=choices.ENERGIA
    )

    temperamento = models.PositiveSmallIntegerField(
        "temperamento", choices=choices.TEMPERAMENTO
    )

    independencia = models.PositiveSmallIntegerField(
        "independência", choices=choices.INDEPENDENCIA
    )

    tolerancia_barulho = models.PositiveSmallIntegerField(
        "tolerância a barulho", choices=choices.TOLERANCIA_BARULHO
    )

    experiencia = models.PositiveSmallIntegerField(
        "experiência exigida do tutor", choices=choices.EXPERIENCIA
    )

    cuidados = models.PositiveSmallIntegerField(
        "cuidados especiais", choices=choices.CUIDADOS
    )

    convive_criancas = models.CharField(
        "convive bem com crianças", max_length=3, choices=choices.CONVIVE
    )

    convive_outros_pets = models.CharField(
        "convive bem com outros pets", max_length=3, choices=choices.CONVIVE
    )

    def __str__(self):
        return self.nome
