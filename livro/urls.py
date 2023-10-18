from django.urls import path
from . import views

urlpatterns = [
    path('manager/', views.manager, name='manager'),
    path('livros/', views.livros, name='livros'),
    path('emprestimos/', views.emprestimos, name='emprestimos'),
    path('emprestimos/<atrasos>/', views.emprestimos, name='emprestimos'),
    path('cadastro_livro/', views.cadastro_livro, name='cadastro_livro'),
    path('editar_livro/<int:info>', views.editar_livro, name='editar_livro'),
    path('excluir_livro/<int:info>', views.excluir_livro, name='excluir_livro'),
    path('cadastro_emprestimo/', views.cadastro_emprestimo, name='cadastro_emprestimo'),
    path('popula_dados/', views.popula_dados, name='popula_dados'),
    path('relatorio_emprestimos/', views.relatorio_emprestimos, name='relatorio_emprestimos'),
    path('relatorio_categorias/', views.relatorio_categorias, name='relatorio_categorias'),
    ]

