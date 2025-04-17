from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import *

class NomeDoModelCreate(CreateView):
    template_name = 'cadastros/cadastro_form.html'
    model = NomeDoModel
    success_url = reverse_lazy('index')  # Redireciona para a lista após o cadastro
    fields = ['nome', 'cpf', 'data_nascimento', 'endereco', 'telefone']
    extra_context = {
        'titulo': 'Cadastrar NomeDoModel'
    }

#CRIAR TODOS OS CREATES (Cadastrar) - após criar as Views, criar as URLS