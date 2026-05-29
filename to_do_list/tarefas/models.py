from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Tarefa(models.Model):

    STATUS_CHOICES = [
        ('a_fazer',     'A Fazer'),
        ('em_andamento','Em Andamento'),
        ('em_revisao',  'Em Revisão'),
        ('concluida',   'Concluída'),
        ('cancelada',   'Cancelada'),
    ]

    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta',  'Alta'),
    ]

    titulo     = models.CharField(max_length=100, verbose_name='Título')
    descricao  = models.TextField(blank=True, null=True, verbose_name='Descrição', max_length=1000)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='a_fazer', verbose_name='Status')
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='media', verbose_name='Prioridade')
    prazo      = models.DateField(null=True, blank=True, verbose_name='Prazo')
    criado_em  = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    usuario    = models.ForeignKey(User, on_delete=models.CASCADE)
    arquivada = models.BooleanField(default=False)
    historico    = HistoricalRecords()

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def __str__(self):
        return self.titulo


    def pode_excluir(self):
        return self.status not in ('concluida', 'cancelada')

    def mudanca_status(self):
        fluxo = {
            'a_fazer':      ['em_andamento', 'cancelada'],
            'em_andamento': ['em_revisao',   'cancelada'],
            'em_revisao':   ['concluida',    'em_andamento'],
            'concluida':    [],
            'cancelada':    [],
        }
        return fluxo.get(self.status, [])