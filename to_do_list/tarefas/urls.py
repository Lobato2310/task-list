from django.urls import path
from . import views


urlpatterns = [
    path('', views.listar_tarefas, name='listar_tarefas'),
    path('cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('nova/', views.criar_tarefa, name='criar_tarefa'),
    path('editar/<int:tarefa_id>/', views.editar_tarefa, name='editar_tarefa'),
    path('concluir/<int:tarefa_id>/', views.alternar_status, name='alternar_status'),
    path('arquivar/<int:tarefa_id>/', views.arquivar_tarefa, name='arquivar_tarefa'),
    path('arquivadas/', views.tarefas_arquivadas, name='tarefas_arquivadas'),
    path('desarquivar/<int:tarefa_id>/', views.desarquivar_tarefa, name='desarquivar_tarefa'),
    path('kanban/', views.kanban_tarefas, name='kanban_tarefas'),
    path('tarefa/<int:tarefa_id>/', views.detalhes_tarefa, name='detalhes_tarefa'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
