from django.contrib import admin
from .models import Tarefa
from simple_history.admin import SimpleHistoryAdmin

class TarefaAdmin(SimpleHistoryAdmin):
    list_display = ('titulo', 'status', 'prioridade', 'prazo', 'usuario', 'criado_em')
admin.site.register(Tarefa, TarefaAdmin)
