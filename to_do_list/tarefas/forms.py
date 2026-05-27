from django.db import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Tarefa


class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'status', 'prioridade', 'prazo']
        
    def clean_prazo(self):
        prazo = self.cleaned_data.get('prazo')
        if prazo and prazo < timezone.now().date():
            raise ValidationError("O prazo não pode ser no passado.")
        return prazo
    