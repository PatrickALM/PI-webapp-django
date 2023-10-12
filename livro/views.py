from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from usuarios.models import Funcionariosdb, Usuariosdb
from livro.models import Livrosdb, Categoriadb , Emprestimosdb
from .forms import LivroForm, FiltroForm,EmprestimoForm
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
        temp_disp = '0'
        temp_order = '0'
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        form = LivroForm()
        filtro = FiltroForm()
        livros = Livrosdb.objects.all()
        if request.method == "POST":
                                   
            temp = request.POST['categoria']
            temp_disp = request.POST['disponibilidade']
            temp_order = request.POST['order']
            filtro = FiltroForm(initial={'categoria':temp, 'disponibilidade':temp_disp, 'order':temp_order})


            # FILTRA CATEGORIA
            if temp == '0':
                livros = Livrosdb.objects.all()
            else:
                livros = Livrosdb.objects.filter(categoria_id = temp)

            # FILTRA DISPONIBILIDADE
            if temp_disp == '2':
                livros = livros.filter(disponibilidade = False)
            elif temp_disp == '1':
                livros = livros.filter(disponibilidade = True)
            
            # ORDENA OS OBJETOS
            if temp_order == '0':
                livros = livros.order_by("-data_cadastro","titulo")
            elif temp_order == '1':
                livros = livros.order_by("data_cadastro", "titulo")
            elif temp_order == '2':
                livros = livros.order_by("titulo")
            elif temp_order == '3':
                livros = livros.order_by("-titulo")
            
        contagem = len(livros)


        
        return render(request, 'livros.html',{'livros':livros, 'form':form, 'filtro':filtro, 'contagem':contagem})
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
            try:
                if request.POST['disponibilidade'] == 'on':
                    livro.disponibilidade = True
                else:
                    livro.disponibilidade = False
            except MultiValueDictKeyError:
                 livro.disponibilidade = False
            livro.ano_de_publicacao = request.POST['ano_de_publicacao']
            livro.ISBN = request.POST['ISBN']
            livro.categoria = Categoriadb.objects.get(nome=request.POST['categoria'])         
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
            form = LivroForm(request.POST, request.FILES)
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
        historico = Emprestimosdb.objects.all()
        form = EmprestimoForm()
        if request.method == "POST":
            pass

        return render(request, 'emprestimos.html',{'historico':historico,'form':form})
    else:
        return redirect('/auth/login/?status=2')
    


def cadastro_emprestimo(request):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        form = EmprestimoForm(request.POST)
        if request.method == "POST":
            if form.is_valid:
                print(Funcionariosdb.objects.get(id=request.session['usuario']))
                emprestimo = Emprestimosdb(
                    id_livro = Livrosdb.objects.get(id=int(form.data['id_livro'])),
                    id_usuario = Usuariosdb.objects.get(id=int(form.data['id_usuario'])),
                    data_retorno_previsto = form.data['data_retorno_previsto'])
                form.save(emprestimo)
                messages.success(request, 'Emprestimo cadastrado com sucesso.')
                return redirect('/livro/emprestimos/')
            else:
                messages.ERROR(request, 'Falha ao cadastrar emprestimo. Verifique as informações e tente novamente.')
                return redirect('/livro/emprestimos/')
    else:
        return redirect('/auth/login/?status=2')

    

    

def popula_tb_livros(request):

    return render('Tabela livros populada com sucesso')