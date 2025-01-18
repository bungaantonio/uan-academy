# lancamentos_pautas/models/Estudante.py
from django.contrib.auth.models import User
from django.db import models


class Estudante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    numero = models.CharField(null=False, blank=False, default="202000375", max_length=9)
    ano_academico = models.IntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
