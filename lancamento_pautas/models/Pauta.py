# lancamentos_pautas/models/Pauta.py
from django.db import models

from lancamento_pautas.models import Disciplina, Estudante, ESCOLHER_MODELO, Nota


class Pauta(models.Model):
    modelo = models.CharField(max_length=1, choices=ESCOLHER_MODELO, null=False, blank=False, default=1)
    descricao = models.TextField(default="Observações a considerar...")

    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    estudantes = models.ManyToManyField(Estudante)
    
    class Meta:
        unique_together = ('modelo', 'disciplina')

    def __str__(self):
        return f"Modelo {self.get_modelo_display()} de {self.disciplina} do professor {self.disciplina.professor}"
