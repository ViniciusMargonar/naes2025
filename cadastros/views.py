from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import (
    Estado, Cidade, Fornecedor, Frota,
    CategoriaItem, Item, ItemPedido, Pedido
)


#################### VIEWS CREATE ####################################################################################################

class EstadoCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Estado
    success_url = reverse_lazy('estado-list')
    fields = ['nome', 'sigla']
    extra_context = {'titulo': 'Cadastrar Estado'}
    
    def form_valid(self, form):
        messages.success(self.request, 'Estado cadastrado com sucesso!')
        return super().form_valid(form)

class CidadeCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Cidade
    success_url = reverse_lazy('cidade-list')
    fields = ['nome', 'estado']
    extra_context = {'titulo': 'Cadastrar Cidade'}
    
    def form_valid(self, form):
        messages.success(self.request, 'Cidade cadastrada com sucesso!')
        return super().form_valid(form)

class FornecedorCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Fornecedor
    success_url = reverse_lazy('fornecedor-list')
    fields = ['nome', 'cnpj', 'telefone', 'email', 'cidade', 'estado']
    extra_context = {'titulo': 'Cadastrar Fornecedor'}
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        messages.success(self.request, 'Fornecedor cadastrado com sucesso!')
        return super().form_valid(form)


class FrotaCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Frota
    success_url = reverse_lazy('frota-list')
    fields = ['prefixo', 'descricao', 'ano']
    extra_context = {'titulo': 'Cadastrar Frota'}
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        messages.success(self.request, 'Frota cadastrada com sucesso!')
        return super().form_valid(form)


class CategoriaItemCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = CategoriaItem
    success_url = reverse_lazy('categoriaitem-list')
    fields = ['nome']
    extra_context = {'titulo': 'Cadastrar Categoria de Item'}
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        messages.success(self.request, 'Categoria cadastrada com sucesso!')
        return super().form_valid(form)


class ItemCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Item
    success_url = reverse_lazy('item-list')
    fields = ['nome', 'categoria']
    extra_context = {'titulo': 'Cadastrar Item'}
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        messages.success(self.request, 'Item cadastrado com sucesso!')
        return super().form_valid(form)


class ItemPedidoCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = ItemPedido
    success_url = reverse_lazy('itempedido-list')
    fields = ['item', 'frota', 'pedido', 'status', 'quantidade', 'valor_unitario']
    extra_context = {'titulo': 'Cadastrar Item do Pedido'}
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        messages.success(self.request, 'Item do pedido cadastrado com sucesso!')
        return super().form_valid(form)


class PedidoCreate(LoginRequiredMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Pedido
    success_url = reverse_lazy('pedido-list')
    fields = ['fornecedor', 'descricao', 'previsao_entrega', 'status']
    extra_context = {'titulo': 'Cadastrar Pedido'}
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        messages.success(self.request, 'Pedido cadastrado com sucesso!')
        return super().form_valid(form)

#################### VIEWS UPDATE ####################################################################################################

class EstadoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Estado
    success_url = reverse_lazy('estado-list')
    fields = ['nome', 'sigla']
    extra_context = {'titulo': 'Atualizar Estado'}
    
    def form_valid(self, form):
        messages.success(self.request, 'Estado atualizado com sucesso!')
        return super().form_valid(form)

class CidadeUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Cidade
    success_url = reverse_lazy('cidade-list')
    fields = ['nome', 'estado']
    extra_context = {'titulo': 'Atualizar Cidade'}
    
    def form_valid(self, form):
        messages.success(self.request, 'Cidade atualizada com sucesso!')
        return super().form_valid(form)

class FornecedorUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Fornecedor
    success_url = reverse_lazy('fornecedor-list')
    fields = ['nome', 'cnpj', 'telefone', 'email', 'cidade']
    extra_context = {'titulo': 'Atualizar Fornecedor'}
    
    def form_valid(self, form):
        messages.success(self.request, 'Fornecedor atualizado com sucesso!')
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        return get_object_or_404(Fornecedor, pk=self.kwargs['pk'])


class FrotaUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Frota
    success_url = reverse_lazy('frota-list')
    fields = ['prefixo', 'descricao', 'ano']
    extra_context = {'titulo': 'Atualizar Frota'}
    
    def form_valid(self, form):
        messages.success(self.request, 'Frota atualizada com sucesso!')
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        return get_object_or_404(Frota, pk=self.kwargs['pk'])


class CategoriaItemUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = CategoriaItem
    success_url = reverse_lazy('categoriaitem-list')
    fields = ['nome']
    extra_context = {'titulo': 'Atualizar Categoria de Item'}
    
    def form_valid(self, form):
        messages.success(self.request, 'Categoria atualizada com sucesso!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(CategoriaItem, pk=self.kwargs['pk'])


class ItemUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Item
    success_url = reverse_lazy('item-list')
    fields = ['nome', 'categoria']
    extra_context = {'titulo': 'Atualizar Item'}
    
    def form_valid(self, form):
        messages.success(self.request, 'Item atualizado com sucesso!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(Item, pk=self.kwargs['pk'])


class PedidoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Pedido
    success_url = reverse_lazy('pedido-list')
    fields = ['fornecedor', 'descricao', 'previsao_entrega', 'status']
    extra_context = {'titulo': 'Atualizar Pedido'}
    
    def form_valid(self, form):
        messages.success(self.request, 'Pedido atualizado com sucesso!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(Pedido, pk=self.kwargs['pk'])


class ItemPedidoUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = ItemPedido
    success_url = reverse_lazy('itempedido-list')
    fields = ['item', 'frota', 'pedido', 'status', 'quantidade', 'valor_unitario']
    extra_context = {'titulo': 'Atualizar Item do Pedido'}
    
    def form_valid(self, form):
        messages.success(self.request, 'Item do pedido atualizado com sucesso!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(ItemPedido, pk=self.kwargs['pk'])


#################### VIEWS DELETE ####################################################################################################

class EstadoDelete(LoginRequiredMixin, DeleteView):
    model = Estado
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('estado-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Exclusão feita com sucesso!')
        return super().form_valid(form)

class CidadeDelete(LoginRequiredMixin, DeleteView):
    model = Cidade
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('cidade-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Exclusão feita com sucesso!')
        return super().form_valid(form)

class FornecedorDelete(LoginRequiredMixin, DeleteView):
    model = Fornecedor
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('fornecedor-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Exclusão feita com sucesso!')
        return super().form_valid(form)

class FrotaDelete(LoginRequiredMixin, DeleteView):
    model = Frota
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('frota-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Exclusão feita com sucesso!')
        return super().form_valid(form)

class CategoriaItemDelete(LoginRequiredMixin, DeleteView):
    model = CategoriaItem
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('categoriaitem-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Exclusão feita com sucesso!')
        return super().form_valid(form)

class ItemDelete(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('item-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Exclusão feita com sucesso!')
        return super().form_valid(form)

class PedidoDelete(LoginRequiredMixin, DeleteView):
    model = Pedido
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('pedido-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Exclusão feita com sucesso!')
        return super().form_valid(form)

class ItemPedidoDelete(LoginRequiredMixin, DeleteView):
    model = ItemPedido
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('itempedido-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Exclusão feita com sucesso!')
        return super().form_valid(form)


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