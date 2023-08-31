from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Funcionariosdb
from common.views import HomeView
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