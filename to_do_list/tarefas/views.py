from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarefa
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import TarefaForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone


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
    status = request.GET.get('status')
    if status:
        tarefas = tarefas.filter(status=status)
    prioridade = request.GET.get('prioridade')
    if prioridade:
        tarefas = tarefas.filter(prioridade=prioridade)
    prazo = request.GET.get('prazo')
    if prazo:
        tarefas = tarefas.order_by('prazo')
    busca = request.GET.get('busca')
    if busca:
        tarefas = tarefas.filter(
            Q(titulo__icontains=busca) | Q(descricao__icontains=busca)
        )
    tarefas = tarefas.filter(arquivada=False)
    paginator = Paginator(tarefas, 5) 
    page_number = request.GET.get('page')
    tarefas = paginator.get_page(page_number)
    if request.headers.get('HX-Request'):
        return render(request, 'tarefas/_lista_tarefas.html', {'tarefas': tarefas})
    return render(request, 'tarefas/listar.html', {'tarefas': tarefas, 'hoje': timezone.now().date()})


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
def arquivar_tarefa(request, tarefa_id):
    tarefa = get_tarefa_por_perfil(request, tarefa_id)
    if tarefa.pode_excluir():
        tarefa.arquivada = True
        tarefa.save()
        return redirect('listar_tarefas')
    else:
        messages.error(request, "Tarefa concluída ou cancelada não pode ser excluída.")
        return redirect('listar_tarefas')
    
@login_required
def tarefas_arquivadas(request, tarefa_id=None):
    if request.user.is_superuser:
        tarefas = Tarefa.objects.filter(arquivada=True)
    elif request.user.is_staff:
        tarefas = Tarefa.objects.filter(arquivada=True)
    else:
        tarefas = Tarefa.objects.filter(usuario=request.user, arquivada=True)
    paginator = Paginator(tarefas, 5)
    page_number = request.GET.get('page')
    tarefas = paginator.get_page(page_number)
    return render(request, 'tarefas/arquivadas.html', {'tarefas': tarefas})

@login_required
def desarquivar_tarefa(request, tarefa_id):
    tarefa = get_tarefa_por_perfil(request, tarefa_id)
    tarefa.arquivada = False
    tarefa.save()
    return redirect('tarefas_arquivadas')

@login_required
def kanban_tarefas(request):
    if request.user.is_superuser:
        tarefas = Tarefa.objects.filter(arquivada=False)
    elif request.user.is_staff:
        tarefas = Tarefa.objects.filter(arquivada=False)
    else:
        tarefas = Tarefa.objects.filter(usuario=request.user, arquivada=False)
    contexto = {
        'a_fazer': tarefas.filter(status='a_fazer'),
        'em_andamento': tarefas.filter(status='em_andamento'),
        'em_revisao': tarefas.filter(status='em_revisao'),
        'concluida': tarefas.filter(status='concluida'),
        'cancelada': tarefas.filter(status='cancelada'),
    }
    return render(request, 'tarefas/kanban.html', contexto)

@login_required
def detalhes_tarefa(request, tarefa_id):
    tarefa = get_tarefa_por_perfil(request, tarefa_id)
    return render(request, 'tarefas/detalhes.html', {'tarefa': tarefa})