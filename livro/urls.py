from django.urls import path
from . import views

urlpatterns = [
    path('manager/', views.manager, name='manager'),
    path('livros/', views.livros, name='livros'),
    path('emprestimos/', views.emprestimos, name='emprestimos'),
    path('usuarios/', views.usuarios, name='usuarios'),

]

