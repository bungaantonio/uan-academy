from django.db import models


class PautaDisponivel(models.Model):
    disponivel = models.BooleanField(default=1)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    notas = models.ForeignKey('Nota', on_delete=models.CASCADE)

    def __str__(self):
        return f"Pauta {self.esta_disponivel()}"

    def esta_disponivel(self):
        return "disponível" if {self.disponivel} == 1 else "indisponível"
