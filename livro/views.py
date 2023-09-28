from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from usuarios.models import Funcionariosdb
from livro.models import Livrosdb, Categoriadb
from .forms import LivroForm, FiltroCategoria
import datetime

def manager(request):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        return render(request, 'main.html')
    else:
        return redirect('/auth/login/?status=2')
    

def livros(request):
    if request.session.get('usuario'):
        temp ='0'
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        form = LivroForm()
        filtro_categoria = FiltroCategoria()
        livros = Livrosdb.objects.all()
        if request.method == "POST":
                        
            temp = request.POST['categoria']

            filtro_categoria = FiltroCategoria(initial={'categoria':temp})
            if temp == '0':
                livros = Livrosdb.objects.all()
            else:
                livros = Livrosdb.objects.filter(categoria_id = temp)

            
            print(temp)
        
        return render(request, 'livros.html',{'livros':livros, 'form':form, 'filtro_categoria':filtro_categoria, 'temp':temp})
    else:
        return redirect('/auth/login/?status=2')

def editar_livro(request, info):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        livro = Livrosdb.objects.get(id=info)
        categorias = Categoriadb.objects.all()
        if request.method == 'POST':
            livro.titulo = request.POST['titulo']
            livro.autor = request.POST['autor']
            # try:
            #     if request.POST['disponibilidade'] == 'on':
            #         livro.disponibilidade = True
            #     else:
            #         livro.disponibilidade = False
            # except MultiValueDictKeyError():
            #      livro.disponibilidade = False
            print(request.POST['disponibilidade'])
            # livro.disponibilidade = request.POST['disponibilidade']
            livro.ano_de_publicacao = request.POST['ano_de_publicacao']
            livro.ISBN = request.POST['ISBN']
            # livro.categoria = Categoriadb.objects.get(nome=request.POST['categoria'])         
            try:
                messages.success(request, 'Livro editado com sucesso.')
                livro.save()
                return redirect('/livro/livros/')
            except:
                messages.ERROR(request, 'Houve um erro inesperado ao editar o livro')
                return redirect('/livro/livros/')
        
        return render(request, 'editar_livro.html',{'livro':livro,'categorias':categorias})
    else:
        return redirect('/auth/login/?status=2')
    
def excluir_livro(request, info):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        try:
            livro = Livrosdb.objects.get(id=info).delete()
            messages.success(request, 'Livro excluido com sucesso.')
            return redirect('/livro/livros/')
        except:
            messages.ERROR(request, 'Houve um erro inesperado ao excluir o livro')
            return redirect('/livro/livros/')
        
    else:
        return redirect('/auth/login/?status=2')

    
def cadastro_livro(request):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        if request.method == 'POST':
            form = LivroForm(request.POST)
            if form.is_valid:
                livro = Livrosdb(
                    titulo = form.data['titulo'],
                    autor = form.data['autor'],
                    ISBN = form.data['ISBN'],
                    ano_de_publicacao = form.data['ano_de_publicacao'],
                    categoria = Categoriadb.objects.get(id=form.data['categoria'])

                )
                form.save(livro)
                messages.success(request, 'Livro cadastrado com sucesso.')
                return redirect('/livro/livros/')
            else:
                messages.ERROR(request, 'Falha ao cadastrar livro. Verifique as informações e tente novamente.')
                return redirect('/livro/livros/')
    else:
        return redirect('/auth/login/?status=2')
    
def emprestimos(request):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        return render(request, 'emprestimos.html')
    else:
        return redirect('/auth/login/?status=2')
    
def usuarios(request):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        return render(request, 'usuarios.html')
    else:
        return redirect('/auth/login/?status=2')
    

def popula_tb_livros(request):

    return render('Tabela livros populada com sucesso')