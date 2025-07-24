from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    Estado, Cidade, Fornecedor, Frota,
    CategoriaItem, Item, ItemPedido, Pedido
)


#################### VIEWS CREATE ####################################################################################################

class EstadoCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Estado
    success_url = reverse_lazy('index')
    fields = ['nome', 'sigla']
    extra_context = {'titulo': 'Cadastrar Estado'}

class CidadeCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Cidade
    success_url = reverse_lazy('index')
    fields = ['nome', 'estado']
    extra_context = {'titulo': 'Cadastrar Cidade'}

class FornecedorCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Fornecedor
    success_url = reverse_lazy('listar-fornecedor')
    fields = ['nome', 'cnpj', 'telefone', 'email', 'cidade', 'estado']
    extra_context = {'titulo': 'Cadastrar Fornecedor'}
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class FrotaCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Frota
    success_url = reverse_lazy('index')
    fields = ['prefixo', 'descricao', 'ano']
    extra_context = {'titulo': 'Cadastrar Frota'}
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class CategoriaItemCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = CategoriaItem
    success_url = reverse_lazy('index')
    fields = ['nome']
    extra_context = {'titulo': 'Cadastrar Categoria de Item'}
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class ItemCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Item
    success_url = reverse_lazy('index')
    fields = ['nome', 'categoria']
    extra_context = {'titulo': 'Cadastrar Item'}
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class ItemPedidoCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = ItemPedido
    success_url = reverse_lazy('index')
    fields = ['item', 'frota', 'pedido', 'status', 'quantidade', 'valor_unitario']
    extra_context = {'titulo': 'Cadastrar Item do Pedido'}
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class PedidoCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Pedido
    success_url = reverse_lazy('index')
    fields = ['fornecedor', 'descricao', 'previsao_entrega', 'status']
    extra_context = {'titulo': 'Cadastrar Pedido'}
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)

#################### VIEWS UPDATE ####################################################################################################

class EstadoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Estado
    success_url = reverse_lazy('index')
    fields = ['nome', 'sigla']
    extra_context = {'titulo': 'Atualizar Estado'}

class CidadeUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Cidade
    success_url = reverse_lazy('index')
    fields = ['nome', 'estado']
    extra_context = {'titulo': 'Atualizar Cidade'}

class FornecedorUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Fornecedor
    success_url = reverse_lazy('listar-fornecedor')
    fields = ['nome', 'cnpj', 'telefone', 'email', 'cidade']
    extra_context = {'titulo': 'Atualizar Fornecedor'}
    def get_object(self, queryset=None):
        return get_object_or_404(Fornecedor, pk=self.kwargs['pk'])


class FrotaUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Frota
    success_url = reverse_lazy('index')
    fields = ['prefixo', 'descricao', 'ano']
    extra_context = {'titulo': 'Atualizar Frota'}
    def get_object(self, queryset=None):
        return get_object_or_404(Frota, pk=self.kwargs['pk'])


class CategoriaItemUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = CategoriaItem
    success_url = reverse_lazy('index')
    fields = ['nome']
    extra_context = {'titulo': 'Atualizar Categoria de Item'}

    def get_object(self, queryset=None):
        return get_object_or_404(CategoriaItem, pk=self.kwargs['pk'])


class ItemUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Item
    success_url = reverse_lazy('index')
    fields = ['nome', 'categoria']
    extra_context = {'titulo': 'Atualizar Item'}

    def get_object(self, queryset=None):
        return get_object_or_404(Item, pk=self.kwargs['pk'])


class PedidoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Pedido
    success_url = reverse_lazy('index')
    fields = ['fornecedor', 'descricao', 'previsao_entrega', 'status']
    extra_context = {'titulo': 'Atualizar Pedido'}

    def get_object(self, queryset=None):
        return get_object_or_404(Pedido, pk=self.kwargs['pk'])


class ItemPedidoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = ItemPedido
    success_url = reverse_lazy('index')
    fields = ['item', 'frota', 'pedido', 'status', 'quantidade', 'valor_unitario']
    extra_context = {'titulo': 'Atualizar Item do Pedido'}

    def get_object(self, queryset=None):
        return get_object_or_404(ItemPedido, pk=self.kwargs['pk'])


#################### VIEWS LIST ####################################################################################################

class EstadoList(LoginRequiredMixin, ListView):
    template_name = 'listas/estado.html'
    model = Estado

class CidadeList(LoginRequiredMixin, ListView):
    template_name = 'listas/cidade.html'
    model = Cidade

class FornecedorList(LoginRequiredMixin, ListView):
    template_name = 'listas/fornecedor.html'
    model = Fornecedor

class FrotaList(LoginRequiredMixin, ListView):
    template_name = 'listas/frota.html'
    model = Frota

class CategoriaItemList(LoginRequiredMixin, ListView):
    template_name = 'listas/categoriaitem.html'
    model = CategoriaItem

class ItemList(LoginRequiredMixin, ListView):
    template_name = 'listas/item.html'
    model = Item

class PedidoList(LoginRequiredMixin, ListView):
    template_name = 'listas/pedido.html'
    model = Pedido

class ItemPedidoList(LoginRequiredMixin, ListView):
    template_name = 'listas/itempedido.html'
    model = ItemPedido

#EXEMPLOS AULA 240425


# class NomeDoModelCreate(LoginRequiredMixin, CreateView):
#     template_name = 'cadastros/form.html'
#     model = NomeDoModel
#     success_url = reverse_lazy('index')  # Redireciona para a lista após o cadastro
#     fields = ['nome', 'cpf', 'data_nascimento', 'endereco', 'telefone']
#     extra_context = {
#         'titulo': 'Cadastrar NomeDoModel'
#     }

# #CRIAR TODOS OS CREATES (Cadastrar) - após criar as Views, criar as URLS

# class NomeDoModelUpdate(LoginRequiredMixin, UpdateView):
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