from django.contrib import admin

from lancamento_pautas.models import Professor, Disciplina, Pauta, Estudante, Nota, PautaDisponivel, Administrador

admin.site.register(Administrador)
admin.site.register(Professor)
admin.site.register(Disciplina)
admin.site.register(Estudante)
admin.site.register(Pauta)
admin.site.register(Nota)
admin.site.register(PautaDisponivel)

