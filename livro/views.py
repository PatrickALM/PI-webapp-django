from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from usuarios.models import Funcionariosdb, Usuariosdb
from livro.models import Livrosdb, Categoriadb , Emprestimosdb
from .forms import LivroForm, FiltroForm,EmprestimoForm
from django.db.models import Count 
import datetime
import json
import pandas as pd
import numpy as np

def manager(request):
    if request.session.get('usuario'):
        
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        emps = Emprestimosdb.objects.all()
        qnt_livros= Livrosdb.objects.all().count()
        qnt_usuarios= Usuariosdb.objects.all().count()
        qnt_emps= emps.count()
        qnt_atrasos= Emprestimosdb.objects.filter(situacao = 'Atrasado').count()

        #data_rank = list(Emprestimosdb.objects.select_related("id_livro","id_usuario").values('id_usuario__id').annotate(dcount=Count('id_usuario__id')).order_by('-dcount'))
        data_rank = list(Emprestimosdb.objects.select_related("id_livro").values('id_livro__id').annotate(dcount=Count('id_livro__id')).order_by('-dcount'))
        for i in range(0,3):
            # ctx = Usuariosdb.objects.filter(id = data_rank[i]['id_usuario__id'])
            ctx = Livrosdb.objects.filter(id = data_rank[i]['id_livro__id'])
            data_rank[i]['nome'] = ctx[0].titulo
        


        print('-'*50)
        print(data_rank[0:3])

        
        return render(request, 'main.html',{'qnt_livros':qnt_livros,'qnt_usuarios':qnt_usuarios,'qnt_emps':qnt_emps,'qnt_atrasos':qnt_atrasos, 'ranking': data_rank[0:3], 'range': range(0,3)
                                            })
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
            
        contagem = livros.count()


        
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

            if (request.FILES.get('imagem')==None and livro.img != "" ):
                livro.img = livro.img
            else:
                livro.img = request.FILES.get('imagem')    
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
    

def emprestimos(request, atrasos='0'):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        historico = Emprestimosdb.objects.all()

        if atrasos == '1':
            historico = Emprestimosdb.objects.filter(situacao = 'Atrasado').order_by('data_saida')

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

    

def relatorio_emprestimos(request):
    if request.session.get('usuario'):
        x = Emprestimosdb.objects.all()
        dados_grafico_usuario = Usuariosdb.objects.all()

        meses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
        data = []
        labels = []
        data_usuario = []
        mes = datetime.datetime.now().month + 1
        ano = datetime.datetime.now().year

        for i in range(12):
            mes -= 1
            if mes == 0:
                mes = 12
                ano -= 1
             
            y = x.filter(data_saida__month = mes, data_saida__year = ano).count()
            z = dados_grafico_usuario.filter(data_cadastro__month = mes, data_cadastro__year = ano).count()


            labels.append(meses[mes-1])
            data.append(y)
            data_usuario.append(z)

        data_json = {'data': data[::-1], 'labels': labels[::-1], 'data_usuario':data_usuario[::-1]}

        return JsonResponse(data_json)
        
    else:
        return redirect('/auth/login/?status=2')


def relatorio_categorias(request):
    data = []
    labels = []

    if request.session.get('usuario'):
        # data = Emprestimosdb.objects.all()
        data_emps = list(Emprestimosdb.objects.select_related("id_livro","id_livro__categoria").values('id_livro__categoria__nome').annotate(dcount=Count('id_livro__categoria__nome')).order_by())
        
        
        # print(data.query)
        # print('-'*20)
        # print(x.nome)

        print(type(data_emps))
        for i in range(0,len(data_emps)):
            labels.append(data_emps[i]['id_livro__categoria__nome'])
            data.append(data_emps[i]['dcount'])
        
        data_json = {'data': data,'labels':labels}
        print(labels)
        print(data)

        return JsonResponse(data_json)
        
    else:
        return redirect('/auth/login/?status=2')




def popula_dados(request):
    if request.session.get('usuario'):
        
        #    Popula tabela de emprestimos para teste
        start = pd.to_datetime('2023-04-01')
        end = pd.to_datetime('2023-10-23')

        for i in range(50):
            saida = start + datetime.timedelta(seconds=np.random.randint(0, int((end - start).total_seconds())))
            retorno = saida + datetime.timedelta(seconds=np.random.randint(0, int((end - saida).total_seconds())))

            emprestimo = Emprestimosdb(
                id_livro = Livrosdb.objects.get(id=np.random.randint(4, 65)),
                id_usuario = Usuariosdb.objects.get(id=np.random.randint(9, 17)),
                id_funcionario = Funcionariosdb.objects.get(id=request.session['usuario']),
                data_saida = saida,
                data_retorno_previsto = retorno
            )
            
            if (end - start) > datetime.timedelta(days = 7):
                emprestimo.situacao = np.random.choice(['Atrasado','Concluido'])
                
            else:
                emprestimo.situacao = 'Em andamento'
            emprestimo.save()









        #    Popula tabela de livros para teste com os dados do dataset encontrado no Kaggle
        # df = pd.read_csv('D:/workspace/UNIVESP/Projeto_Integrador_II_2023/db_livros.csv', sep=';')
        # for i in range(len(df)):
        #     codigo = ''
        #     if df.loc[i, "status"] == 'available':
        #         disp = True
        #     else:
        #         disp = False
        #     for x in range(13):
        #         codigo += str(np.random.randint(0, 10))
        #     livro = Livrosdb(
        #         titulo = df.loc[i, "title"],
        #         autor = df.loc[i, "author"],
        #         ISBN = codigo,
        #         ano_de_publicacao = np.random.randint(1990, 2023),
        #         categoria = Categoriadb.objects.get(nome=df.loc[i, "category"]),
        #         disponibilidade = disp
        #     )
        #     livro.save()
        #     print(df.loc[i, "title"], df.loc[i, "author"])

        return redirect('/livro/livros/')
    else:
        return redirect('/auth/login/?status=2')