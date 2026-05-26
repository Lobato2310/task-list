from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_tarefas, name='listar_tarefas'),
    path('nova/', views.criar_tarefa, name='criar_tarefa'),
    path('editar/<int:tarefa_id>/', views.editar_tarefa, name='editar_tarefa'),
    path('concluir/<int:tarefa_id>/', views.alternar_status, name='alternar_status'),
    path('excluir/<int:tarefa_id>/', views.excluir_tarefa, name='excluir_tarefa'),
]

"""commit error"""