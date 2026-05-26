from django.db import models


class Tarefa(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    concluida = models.BooleanField(default=False, verbose_name="Concluída")
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo