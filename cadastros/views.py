from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import *

class PedidoCreateView(CreateView):
    model = Pedido
    fields = ['cliente', 'descricao', 'data_entrega', 'status']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('index')
    extra_context = {'titulo': 'Cadastrar Pedido'}

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)













class NomeDoModelCreate(CreateView):
    template_name = 'cadastros/form.html'
    model = NomeDoModel
    success_url = reverse_lazy('index')  # Redireciona para a lista após o cadastro
    fields = ['nome', 'cpf', 'data_nascimento', 'endereco', 'telefone']
    extra_context = {
        'titulo': 'Cadastrar NomeDoModel'
    }

#CRIAR TODOS OS CREATES (Cadastrar) - após criar as Views, criar as URLS

class NomeDoModelUpdate(UpdateView):
    template_name = 'cadastros/form.html'
    model = NomeDoModel
    success_url = reverse_lazy('index')  # Redireciona para a lista após a atualização
    fields = ['nome', 'cpf', 'data_nascimento', 'endereco', 'telefone']
    extra_context = {
        'titulo': 'Atualizar NomeDoModel'
    }

    def get_object(self, queryset=None):
        self.object = get_object_or_404(NomeDoModel, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object  

#CRIAR TODOS OS UPDATES (Atualizar) - após criar as Views, criar as URLS