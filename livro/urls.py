from django.urls import path
from . import views

urlpatterns = [
    path('manager/', views.manager, name='manager'),
    path('livros/', views.livros, name='livros'),
    path('emprestimos/', views.emprestimos, name='emprestimos'),
    path('cadastro_livro/', views.cadastro_livro, name='cadastro_livro'),
    path('editar_livro/<int:info>', views.editar_livro, name='editar_livro'),
    path('excluir_livro/<int:info>', views.excluir_livro, name='excluir_livro'),
    path('cadastro_emprestimo/', views.cadastro_emprestimo, name='cadastro_emprestimo'),
    ]

