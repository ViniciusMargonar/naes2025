from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin

def login_user(request):
    """View para login do usuário"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
            # Redireciona para a página inicial ou página solicitada
            next_page = request.GET.get('next', '/')
            return redirect(next_page)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'usuario/login.html')

def logout_user(request):
    """View para logout do usuário"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')

class UsuarioCreate(SuccessMessageMixin, CreateView):
    """View para criar usuário"""
    model = User
    form_class = UserCreationForm
    template_name = 'usuario/form.html'
    success_url = reverse_lazy('login')
    success_message = "Usuário cadastrado com sucesso! Faça login para continuar."
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastrar Usuário'
        return context
