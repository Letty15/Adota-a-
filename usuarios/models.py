from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    endereco = models.CharField(
        max_length=255,
        blank=True
    )

    cidade = models.CharField(
        max_length=100,
        blank=True
    )

    foto = models.ImageField(
        upload_to="perfil/",
        default="perfil/default.png",
        blank=True
    )

    def __str__(self):
        return self.usuario.username