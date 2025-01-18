# lancamentos_pautas/models/Disciplina.py
from django.db import models

from lancamento_pautas.models import ESCOLHER_TURNO, Professor


class Disciplina(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    codigo = models.CharField(max_length=10, null=False, blank=False)
    turno = models.IntegerField(choices=ESCOLHER_TURNO, null=False, blank=False)

    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    estudantes = models.ManyToManyField('Estudante', related_name='disciplinas')

    def __str__(self):
        return self.nome
