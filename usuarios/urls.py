from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('valida_login/', views.valida_login, name='valida_login'),
    path('sair/', views.sair, name='sair'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('cadastro_usuario/', views.cadastro_usuario, name='cadastro_usuario'),
    path('editar_usuario/<int:info>', views.editar_usuario, name='editar_usuario'),
    path('excluir_usuario/<int:info>', views.excluir_usuario, name='excluir_usuario'),

]
