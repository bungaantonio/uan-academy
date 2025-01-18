from django.contrib.auth.models import User

ESCOLHER_TURNO = (
    (1, 'Manhã'),
    (2, 'Tarde')
)

ESCOLHER_CONDICAO = [
    (1, 'Regular'),
    (2, 'Prescrito'),
]

ESCOLHER_MODELO = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C')
]

from .Administrador import Administrador
from .Professor import Professor
from .Disciplina import Disciplina
from .Estudante import Estudante
from .Pauta import Pauta
from .Nota import Nota
from .PautaDisponivel import PautaDisponivel
