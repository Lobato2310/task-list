from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Tarefa
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class TarefaForm(forms.ModelForm):
    prazo = forms.DateField(
        required=False,
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
    )
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'status', 'prioridade', 'prazo']
    def clean_prazo(self):
        prazo = self.cleaned_data.get('prazo')
        if prazo and prazo < timezone.now().date():
            raise ValidationError("O prazo não pode ser no passado.")
        return prazo
    