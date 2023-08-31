from django.shortcuts import render, redirect
from django.http import HttpResponse
from usuarios.models import Funcionariosdb


def manager(request):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        return render(request, 'main.html')
    else:
        return redirect('/auth/login/?status=2')
    

def livros(request):
    if request.session.get('usuario'):
        usuario = Funcionariosdb.objects.get(id=request.session['usuario'])
        return render(request, 'livros.html')
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
    