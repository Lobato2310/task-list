from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarefa

def listar_tarefas(request):
    tarefas = Tarefa.objects.all().order_by('criado_em')
    return render(request, 'tarefas/listar.html', {'tarefas': tarefas})

def criar_tarefa(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        Tarefa.objects.create(titulo=titulo, descricao=descricao)
        return redirect('listar_tarefas')
    return render(request, 'tarefas/form.html')

def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    if request.method == 'POST':
        tarefa.titulo = request.POST.get('titulo')
        tarefa.descricao = request.POST.get('descricao')
        tarefa.save()
        return redirect('listar_tarefas')
    return render(request, 'tarefas/form.html', {'tarefa' : tarefa})

def alternar_status(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    tarefa.concluida = not tarefa.concluida
    tarefa.save()
    return redirect('listar_tarefas')

def excluir_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    tarefa.delete()
    return redirect('listar_tarefas')