from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarefa
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


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
    tarefas = Tarefa.objects.filter(usuario=request.user)
    return render(request, 'tarefas/listar.html', {'tarefas': tarefas})

@login_required
def criar_tarefa(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        Tarefa.objects.create(titulo=titulo, descricao=descricao, usuario=request.user)
        return redirect('listar_tarefas')
    return render(request, 'tarefas/form.html')

@login_required
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
    if request.method == 'POST':
        tarefa.titulo = request.POST.get('titulo')
        tarefa.descricao = request.POST.get('descricao')
        tarefa.save()
        return redirect('listar_tarefas')
    return render(request, 'tarefas/form.html', {'tarefa' : tarefa})

@login_required
def alternar_status(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
    tarefa.concluida = not tarefa.concluida
    tarefa.save()
    return redirect('listar_tarefas')

@login_required
def excluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
    tarefa.delete()
    return redirect('listar_tarefas')