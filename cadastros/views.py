from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import (
    Estado, Cidade, Fornecedor, Frota,
    CategoriaItem, Item, ItemPedido, Pedido
)

#################### VIEWS CREATE ####################################################################################################

class EstadoCreate(CreateView):
    template_name = 'cadastros/form.html'
    model = Estado
    success_url = reverse_lazy('index')
    fields = ['nome', 'sigla']
    extra_context = {'titulo': 'Cadastrar Estado'}


class CidadeCreate(CreateView):
    template_name = 'cadastros/form.html'
    model = Cidade
    success_url = reverse_lazy('index')
    fields = ['nome', 'estado']
    extra_context = {'titulo': 'Cadastrar Cidade'}


class FornecedorCreate(CreateView):
    template_name = 'cadastros/form.html'
    model = Fornecedor
    success_url = reverse_lazy('index')
    fields = ['nome', 'cnpj', 'telefone', 'email', 'cidade', 'estado']
    extra_context = {'titulo': 'Cadastrar Fornecedor'}

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class FrotaCreate(CreateView):
    template_name = 'cadastros/form.html'
    model = Frota
    success_url = reverse_lazy('index')
    fields = ['prefixo', 'descricao', 'ano']
    extra_context = {'titulo': 'Cadastrar Frota'}

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class CategoriaItemCreate(CreateView):
    template_name = 'cadastros/form.html'
    model = CategoriaItem
    success_url = reverse_lazy('index')
    fields = ['nome']
    extra_context = {'titulo': 'Cadastrar Categoria de Item'}

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class ItemCreate(CreateView):
    template_name = 'cadastros/form.html'
    model = Item
    success_url = reverse_lazy('index')
    fields = ['nome', 'categoria']
    extra_context = {'titulo': 'Cadastrar Item'}

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class ItemPedidoCreate(CreateView):
    template_name = 'cadastros/form.html'
    model = ItemPedido
    success_url = reverse_lazy('index')
    fields = ['item', 'frota', 'pedido', 'status', 'quantidade', 'valor_unitario']
    extra_context = {'titulo': 'Cadastrar Item do Pedido'}

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class PedidoCreate(CreateView):
    template_name = 'cadastros/form.html'
    model = Pedido
    success_url = reverse_lazy('index')
    fields = ['fornecedor', 'descricao', 'previsao_entrega', 'status']
    extra_context = {'titulo': 'Cadastrar Pedido'}

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)

#################### VIEWS UPDATE ####################################################################################################

from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import (
    Estado, Cidade, Fornecedor, Frota,
    CategoriaItem, Item, Pedido, ItemPedido
)


class EstadoUpdate(UpdateView):
    template_name = 'cadastros/form.html'
    model = Estado
    success_url = reverse_lazy('index')
    fields = ['nome', 'sigla']
    extra_context = {'titulo': 'Atualizar Estado'}


class CidadeUpdate(UpdateView):
    template_name = 'cadastros/form.html'
    model = Cidade
    success_url = reverse_lazy('index')
    fields = ['nome', 'estado']
    extra_context = {'titulo': 'Atualizar Cidade'}


class FornecedorUpdate(UpdateView):
    template_name = 'cadastros/form.html'
    model = Fornecedor
    success_url = reverse_lazy('index')
    fields = ['nome', 'cnpj', 'telefone', 'email', 'cidade']
    extra_context = {'titulo': 'Atualizar Fornecedor'}

    def get_object(self, queryset=None):
        return get_object_or_404(Fornecedor, pk=self.kwargs['pk'], criado_por=self.request.user)


class FrotaUpdate(UpdateView):
    template_name = 'cadastros/form.html'
    model = Frota
    success_url = reverse_lazy('index')
    fields = ['prefixo', 'descricao', 'ano']
    extra_context = {'titulo': 'Atualizar Frota'}

    def get_object(self, queryset=None):
        return get_object_or_404(Frota, pk=self.kwargs['pk'], criado_por=self.request.user)


class CategoriaItemUpdate(UpdateView):
    template_name = 'cadastros/form.html'
    model = CategoriaItem
    success_url = reverse_lazy('index')
    fields = ['nome']
    extra_context = {'titulo': 'Atualizar Categoria de Item'}

    def get_object(self, queryset=None):
        return get_object_or_404(CategoriaItem, pk=self.kwargs['pk'], criado_por=self.request.user)


class ItemUpdate(UpdateView):
    template_name = 'cadastros/form.html'
    model = Item
    success_url = reverse_lazy('index')
    fields = ['nome', 'categoria']
    extra_context = {'titulo': 'Atualizar Item'}

    def get_object(self, queryset=None):
        return get_object_or_404(Item, pk=self.kwargs['pk'], criado_por=self.request.user)


class PedidoUpdate(UpdateView):
    template_name = 'cadastros/form.html'
    model = Pedido
    success_url = reverse_lazy('index')
    fields = ['fornecedor', 'descricao', 'previsao_entrega', 'status']
    extra_context = {'titulo': 'Atualizar Pedido'}

    def get_object(self, queryset=None):
        return get_object_or_404(Pedido, pk=self.kwargs['pk'], criado_por=self.request.user)


class ItemPedidoUpdate(UpdateView):
    template_name = 'cadastros/form.html'
    model = ItemPedido
    success_url = reverse_lazy('index')
    fields = ['item', 'frota', 'pedido', 'status', 'quantidade', 'valor_unitario']
    extra_context = {'titulo': 'Atualizar Item do Pedido'}

    def get_object(self, queryset=None):
        return get_object_or_404(ItemPedido, pk=self.kwargs['pk'], criado_por=self.request.user)

#EXEMPLOS AULA 240425
# class NomeDoModelCreate(CreateView):
#     template_name = 'cadastros/form.html'
#     model = NomeDoModel
#     success_url = reverse_lazy('index')  # Redireciona para a lista após o cadastro
#     fields = ['nome', 'cpf', 'data_nascimento', 'endereco', 'telefone']
#     extra_context = {
#         'titulo': 'Cadastrar NomeDoModel'
#     }

# #CRIAR TODOS OS CREATES (Cadastrar) - após criar as Views, criar as URLS

# class NomeDoModelUpdate(UpdateView):
#     template_name = 'cadastros/form.html'
#     model = NomeDoModel
#     success_url = reverse_lazy('index')  # Redireciona para a lista após a atualização
#     fields = ['nome', 'cpf', 'data_nascimento', 'endereco', 'telefone']
#     extra_context = {
#         'titulo': 'Atualizar NomeDoModel'
#     }

#     def get_object(self, queryset=None):
#         self.object = get_object_or_404(NomeDoModel, pk=self.kwargs['pk'], usuario=self.request.user)
#         return self.object  

# #CRIAR TODOS OS UPDATES (Atualizar) - após criar as Views, criar as URLS