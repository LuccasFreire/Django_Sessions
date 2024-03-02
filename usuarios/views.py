from hashlib import sha256
from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario
from django.shortcuts import redirect
# Create your views here.

def login(request):
  status = request.GET.get('status')
  return render(request, 'login.html', {'status': status})

def cadastro(request):
  status = request.GET.get('status')
  return render(request, 'cadastro.html', {'status': status})

def valida_cadastro(request):
  nome = request.POST.get('nome')
  email = request.POST.get('email')
  password = request.POST.get('password')

  #Checa se o campo está vazio ou com whitespace
  if len(nome.strip()) == 0 or len(email.strip()) == 0:
    return redirect('/auth/cadastro?status=1')
  
  if len(password) < 8:
    return redirect('/auth/cadastro?status=2')
  
  usuario = Usuario.objects.filter(email=email)

  if len(usuario) > 0:
    return redirect('/auth/cadastro/?status=3')
  
  try:
    password = sha256(password.encode()).hexdigest()
    usuario = Usuario(nome = nome, email=email, senha = password)
    usuario.save()
    return redirect('/auth/cadastro/?status=0')
  except:
    return redirect('/auth/cadastro/?status=4')
  
  #nome: teste
  #email: teste@gmail.com
  #senha: testeteste

def valida_login(request):
  email = request.POST.get('email')
  password = request.POST.get('password')
  password = sha256(password.encode()).hexdigest()

  usuario = Usuario.objects.filter(email = email).filter(senha = password)
  
  if len(usuario) == 0:
    return redirect('/auth/login/?status=1')
  elif len(usuario) > 0:
    request.session['logado'] = True
    request.session['usuario_id'] = usuario[0].id
    return redirect('/plataforma/home')

def sair(request):
  #request.session.flush()
  try:
    del request.session['logado']
    return redirect('/auth/login/')
  except:
    return redirect('/auth/login/?status=3')