# lancamentos_pautas/models/Nota.py
from django.db import models

from lancamento_pautas.models import Pauta, Estudante


class Nota(models.Model):
    pauta = models.ForeignKey('Pauta', on_delete=models.CASCADE, related_name="notas")
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)

    AC1 = models.FloatField(default=0, null=False, blank=False)
    AC2 = models.FloatField(default=0, null=False, blank=False)
    PF1 = models.FloatField(default=0, null=False, blank=False)
    PF2 = models.FloatField(default=0, null=False, blank=False)

    class Meta:
        unique_together = ('pauta', 'estudante')

    def media_semestral(self):
        return (self.AC1 + self.AC2 + self.PF1 + self.PF2) / 4

    def resultado_final(self):
        return "DES" if self.media_semestral() >= 13.5 else "EXM"

    def __str__(self):
        return f"Notas de {self.estudante.user.first_name} {self.estudante.user.last_name} no Modelo {self.pauta.modelo}"
