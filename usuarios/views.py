from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Funcionariosdb,Usuariosdb
from common.views import HomeView
from .forms import UsuarioForm



def login(request):
    status = request.GET.get('status')
    
    return render(request, HomeView.template_name, {'status': status})


def valida_login(request):
    email= request.POST.get('login_email')
    senha= request.POST.get('login_senha')
    
    
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
        dados_usuarios = Usuariosdb.objects.all().order_by('nome')

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
                    email = form.data['email'],
                    telefone = form.data['telefone'],
                    matricula = form.data['matricula']

                )
                try:
                    form.save(cadastro)
                    messages.success(request, 'Usuário cadastrado com sucesso.')
                    return redirect('/auth/usuarios/')
                except:
                    for error in form.errors:
                        messages.error(request, form.errors[error])
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
            dados_usuario.email = request.POST['email']
            dados_usuario.telefone = request.POST['telefone']
            dados_usuario.matricula = request.POST['matricula']
                   
            try:
                dados_usuario.save()
                messages.success(request, 'Cadastro de usuario editado com sucesso.')
                return redirect('/auth/usuarios/')
            except:
                messages.error(request, 'Certifique-se de que as informações são válidas para editar o cadastro de usuário.')
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