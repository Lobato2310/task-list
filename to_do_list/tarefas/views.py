from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarefa
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import TarefaForm

def get_tarefa_por_perfil(request, tarefa_id):
    if request.user.is_superuser:
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    elif request.user.is_staff:
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    else:
        tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
    return tarefa

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/cadastrar.html', {'form': form})

@login_required
def listar_tarefas(request):
    if request.user.is_superuser:
        tarefas = Tarefa.objects.all()
    elif request.user.is_staff:
        tarefas = Tarefa.objects.all()
    else:
        tarefas = Tarefa.objects.filter(usuario=request.user)

    return render(request, 'tarefas/listar.html', {'tarefas': tarefas})

@login_required
def criar_tarefa(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = request.user
            tarefa.save()
            return redirect('listar_tarefas')
    else:
        form = TarefaForm()
    return render(request, 'tarefas/form.html', {'form': form})

@login_required
def editar_tarefa(request, tarefa_id):
    tarefa = get_tarefa_por_perfil(request, tarefa_id)

    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return redirect('listar_tarefas')
    else:
        form = TarefaForm(instance=tarefa)
    return render(request, 'tarefas/form.html', {'form': form})

@login_required
def alternar_status(request, tarefa_id):
    tarefa = get_tarefa_por_perfil(request, tarefa_id)
    novo_status = request.POST.get('novo_status')  
    if novo_status in tarefa.mudanca_status():
        tarefa.status = novo_status
        tarefa.save()
    else:
        messages.error(request, 'Transição de status não permitida.')
    return redirect('listar_tarefas')

@login_required
def excluir_tarefa(request, tarefa_id):
    tarefa = get_tarefa_por_perfil(request, tarefa_id)
    if tarefa.pode_excluir():
        tarefa.delete()
        return redirect('listar_tarefas')
    else:
        messages.error(request, "Tarefa concluída ou cancelada não pode ser excluída.")
        return redirect('listar_tarefas')
    