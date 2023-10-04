from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Funcionariosdb,Usuariosdb
from common.views import HomeView
from .forms import UsuarioForm
#from hashlib import sha256


def login(request):
    status = request.GET.get('status')
    
    return render(request, HomeView.template_name, {'status': status})

def cadastro(request):
    return HttpResponse('Função CAdastro')

def valida_login(request):
    email= request.POST.get('login_email')
    senha= request.POST.get('login_senha')
    #senha = sha256(senha.encode()).hexadigest()

    usuario = Funcionariosdb.objects.filter(email=email).filter(senha=senha)

    if len(usuario)==0:
        return redirect('/auth/login/?status=1')
    elif len(usuario) > 0:
        request.session['usuario'] = usuario[0].id
        return redirect('/livro/manager/?id_usuario={request.session["usuario"]}')

    
def sair(request):
    request.session.flush()
    return redirect('/auth/login/')


def usuarios(request):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        form = UsuarioForm
        dados_usuarios = Usuariosdb.objects.all()

        return render(request, 'usuarios.html',{'form':form,'dados_usuarios':dados_usuarios})
    else:
        return redirect('/auth/login/?status=2')
    
def cadastro_usuario(request):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        if request.method == 'POST':
            form = UsuarioForm(request.POST)
            if form.is_valid:
                cadastro = Usuariosdb(
                    nome = form.data['nome'],
                    sobrenome = form.data['sobrenome'],
                    endereco = form.data['endereco'],
                    telefone = form.data['telefone'],
                    matricula = form.data['matricula']

                )
                form.save(cadastro)
                messages.success(request, 'Usuário cadastrado com sucesso.')
                return redirect('/auth/usuarios/')
            else:
                messages.ERROR(request, 'Falha ao cadastrar usuário. Verifique as informações e tente novamente.')
                return redirect('/auth/usuarios/')
    else:
        return redirect('/auth/login/?status=2')
    

def editar_usuario(request, info):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        dados_usuario = Usuariosdb.objects.get(id=info)
        
        if request.method == 'POST':
            dados_usuario.nome = request.POST['nome']
            dados_usuario.sobrenome = request.POST['sobrenome']
            dados_usuario.endereco = request.POST['endereco']
            dados_usuario.telefone = request.POST['telefone']
            dados_usuario.matricula = request.POST['matricula']
                   
            try:
                dados_usuario.save()
                messages.success(request, 'Cadastro de usuario editado com sucesso.')
                return redirect('/auth/usuarios/')
            except:
                messages.ERROR(request, 'Houve um erro inesperado ao editar o cadastro de usuario')
                return redirect('/auth/usuarios/')
        
        return render(request, 'editar_usuario.html',{'dados_usuario':dados_usuario})
    else:
        return redirect('/auth/login/?status=2')

def excluir_usuario(request, info):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        try:
            Usuariosdb.objects.get(id=info).delete()
            messages.success(request, 'Cadastro de usuario excluido com sucesso.')
            return redirect('/auth/usuarios/')
        except:
            messages.ERROR(request, 'Houve um erro inesperado ao excluir o cadastro de usuario')
            return redirect('/auth/usuarios/')
        
    else:
        return redirect('/auth/login/?status=2')