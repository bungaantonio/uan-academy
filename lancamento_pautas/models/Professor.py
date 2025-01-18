# lancamentos_pautas/models/Professor.py
from django.contrib.auth.models import User
from django.db import models


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    especialidade = models.CharField(max_length=100, null=False, blank=False)
    exp = models.IntegerField(null=False, blank=False, default=3)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
