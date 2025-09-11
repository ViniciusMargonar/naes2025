from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from .models import (
    Estado, Cidade, Fornecedor, Frota,
    CategoriaItem, Item, ItemPedido, Pedido
)


class SuccessDeleteMixin:
    success_message = "Registro excluído com sucesso!"
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class OwnerRequiredMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if hasattr(obj, 'criado_por') and obj.criado_por != self.request.user:
            raise PermissionDenied("Você não tem permissão para editar/excluir este registro.")
        return obj


#################### VIEWS CREATE ####################################################################################################

class EstadoCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Estado
    success_url = reverse_lazy('estado-list')
    fields = ['nome', 'sigla']
    extra_context = {'titulo': 'Cadastrar Estado'}
    success_message = "Estado cadastrado com sucesso!"

class CidadeCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Cidade
    success_url = reverse_lazy('cidade-list')
    fields = ['nome', 'estado']
    extra_context = {'titulo': 'Cadastrar Cidade'}
    success_message = "Cidade cadastrada com sucesso!"

class FornecedorCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Fornecedor
    success_url = reverse_lazy('fornecedor-list')
    fields = ['nome', 'cnpj', 'telefone', 'email', 'cidade', 'estado']
    extra_context = {'titulo': 'Cadastrar Fornecedor'}
    success_message = "Fornecedor cadastrado com sucesso!"
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class FrotaCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Frota
    success_url = reverse_lazy('frota-list')
    fields = ['prefixo', 'descricao', 'ano']
    extra_context = {'titulo': 'Cadastrar Frota'}
    success_message = "Frota cadastrada com sucesso!"
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class CategoriaItemCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = CategoriaItem
    success_url = reverse_lazy('categoriaitem-list')
    fields = ['nome']
    extra_context = {'titulo': 'Cadastrar Categoria de Item'}
    success_message = "Categoria cadastrada com sucesso!"
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class ItemCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Item
    success_url = reverse_lazy('item-list')
    fields = ['nome', 'categoria']
    extra_context = {'titulo': 'Cadastrar Item'}
    success_message = "Item cadastrado com sucesso!"
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class ItemPedidoCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = ItemPedido
    success_url = reverse_lazy('itempedido-list')
    fields = ['item', 'frota', 'pedido', 'status', 'quantidade', 'valor_unitario']
    extra_context = {'titulo': 'Cadastrar Item do Pedido'}
    success_message = "Item do pedido cadastrado com sucesso!"
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class PedidoCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'cadastros/form.html'
    model = Pedido
    success_url = reverse_lazy('pedido-list')
    fields = ['fornecedor', 'descricao', 'previsao_entrega', 'status']
    extra_context = {'titulo': 'Cadastrar Pedido'}
    success_message = "Pedido cadastrado com sucesso!"
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)

#################### VIEWS UPDATE ####################################################################################################

class EstadoUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Estado
    success_url = reverse_lazy('estado-list')
    fields = ['nome', 'sigla']
    extra_context = {'titulo': 'Atualizar Estado'}
    success_message = "Estado atualizado com sucesso!"

class CidadeUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Cidade
    success_url = reverse_lazy('cidade-list')
    fields = ['nome', 'estado']
    extra_context = {'titulo': 'Atualizar Cidade'}
    success_message = "Cidade atualizada com sucesso!"

class FornecedorUpdate(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Fornecedor
    success_url = reverse_lazy('fornecedor-list')
    fields = ['nome', 'cnpj', 'telefone', 'email', 'cidade']
    extra_context = {'titulo': 'Atualizar Fornecedor'}
    success_message = "Fornecedor atualizado com sucesso!"


class FrotaUpdate(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Frota
    success_url = reverse_lazy('frota-list')
    fields = ['prefixo', 'descricao', 'ano']
    extra_context = {'titulo': 'Atualizar Frota'}
    success_message = "Frota atualizada com sucesso!"


class CategoriaItemUpdate(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = CategoriaItem
    success_url = reverse_lazy('categoriaitem-list')
    fields = ['nome']
    extra_context = {'titulo': 'Atualizar Categoria de Item'}
    success_message = "Categoria atualizada com sucesso!"


class ItemUpdate(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Item
    success_url = reverse_lazy('item-list')
    fields = ['nome', 'categoria']
    extra_context = {'titulo': 'Atualizar Item'}
    success_message = "Item atualizado com sucesso!"


class PedidoUpdate(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = Pedido
    success_url = reverse_lazy('pedido-list')
    fields = ['fornecedor', 'descricao', 'previsao_entrega', 'status']
    extra_context = {'titulo': 'Atualizar Pedido'}
    success_message = "Pedido atualizado com sucesso!"


class ItemPedidoUpdate(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = ItemPedido
    success_url = reverse_lazy('itempedido-list')
    fields = ['item', 'frota', 'pedido', 'status', 'quantidade', 'valor_unitario']
    extra_context = {'titulo': 'Atualizar Item do Pedido'}
    success_message = "Item do pedido atualizado com sucesso!"


#################### VIEWS DELETE ####################################################################################################

class EstadoDelete(LoginRequiredMixin, SuccessDeleteMixin, DeleteView):
    model = Estado
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('estado-list')
    success_message = "Estado excluído com sucesso!"

class CidadeDelete(LoginRequiredMixin, SuccessDeleteMixin, DeleteView):
    model = Cidade
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('cidade-list')
    success_message = "Cidade excluída com sucesso!"

class FornecedorDelete(LoginRequiredMixin, OwnerRequiredMixin, SuccessDeleteMixin, DeleteView):
    model = Fornecedor
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('fornecedor-list')
    success_message = "Fornecedor excluído com sucesso!"

class FrotaDelete(LoginRequiredMixin, OwnerRequiredMixin, SuccessDeleteMixin, DeleteView):
    model = Frota
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('frota-list')
    success_message = "Frota excluída com sucesso!"

class CategoriaItemDelete(LoginRequiredMixin, OwnerRequiredMixin, SuccessDeleteMixin, DeleteView):
    model = CategoriaItem
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('categoriaitem-list')
    success_message = "Categoria excluída com sucesso!"

class ItemDelete(LoginRequiredMixin, OwnerRequiredMixin, SuccessDeleteMixin, DeleteView):
    model = Item
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('item-list')
    success_message = "Item excluído com sucesso!"

class PedidoDelete(LoginRequiredMixin, OwnerRequiredMixin, SuccessDeleteMixin, DeleteView):
    model = Pedido
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('pedido-list')
    success_message = "Pedido excluído com sucesso!"

class ItemPedidoDelete(LoginRequiredMixin, OwnerRequiredMixin, SuccessDeleteMixin, DeleteView):
    model = ItemPedido
    template_name = 'cadastros/confirm_delete.html'
    success_url = reverse_lazy('itempedido-list')
    success_message = "Item do pedido excluído com sucesso!"


#################### VIEWS LIST ####################################################################################################

class EstadoList(LoginRequiredMixin, ListView):
    template_name = 'listas/estado.html'
    model = Estado
    context_object_name = 'estados'
    
    def get_queryset(self):
        # Estados são compartilhados, não precisam filtro por usuário
        return Estado.objects.all().order_by('nome')


class CidadeList(LoginRequiredMixin, ListView):
    template_name = 'listas/cidade.html'
    model = Cidade
    context_object_name = 'cidades'
    
    def get_queryset(self):
        # ✅ OTIMIZAÇÃO: select_related para evitar N+1 queries
        return Cidade.objects.select_related('estado').order_by('nome')


class FornecedorList(LoginRequiredMixin, ListView):
    template_name = 'listas/fornecedor.html'
    model = Fornecedor
    context_object_name = 'fornecedores'
    
    def get_queryset(self):
        # ✅ OTIMIZAÇÃO: select_related + filtro por usuário
        return Fornecedor.objects.select_related(
            'cidade', 
            'estado', 
            'criado_por'
        ).filter(
            criado_por=self.request.user
        ).order_by('-id')  # Usar -id em vez de -criado_em


class FrotaList(LoginRequiredMixin, ListView):
    template_name = 'listas/frota.html'
    model = Frota
    context_object_name = 'frotas'
    
    def get_queryset(self):
        # ✅ FILTRO por usuário + ordenação
        return Frota.objects.select_related('criado_por').filter(
            criado_por=self.request.user
        ).order_by('-id')  # Usar -id em vez de -criado_em


class CategoriaItemList(LoginRequiredMixin, ListView):
    template_name = 'listas/categoriaitem.html'
    model = CategoriaItem
    context_object_name = 'categorias'
    
    def get_queryset(self):
        # ✅ FILTRO por usuário + ordenação
        return CategoriaItem.objects.select_related('criado_por').filter(
            criado_por=self.request.user
        ).order_by('nome')


class ItemList(LoginRequiredMixin, ListView):
    template_name = 'listas/item.html'
    model = Item
    context_object_name = 'itens'
    
    def get_queryset(self):
        # ✅ OTIMIZAÇÃO: select_related para categoria + filtro por usuário
        return Item.objects.select_related(
            'categoria', 
            'criado_por'
        ).filter(
            criado_por=self.request.user
        ).order_by('nome')


class PedidoList(LoginRequiredMixin, ListView):
    template_name = 'listas/pedido.html'
    model = Pedido
    context_object_name = 'pedidos'
    
    def get_queryset(self):
        # ✅ OTIMIZAÇÃO: select_related para fornecedor + filtro por usuário
        return Pedido.objects.select_related(
            'fornecedor', 
            'criado_por'
        ).filter(
            criado_por=self.request.user
        ).order_by('-data_pedido')  # Usar -data_pedido que existe no modelo


class ItemPedidoList(LoginRequiredMixin, ListView):
    template_name = 'listas/itempedido.html'
    model = ItemPedido
    context_object_name = 'itens_pedido'
    
    def get_queryset(self):
        # ✅ OTIMIZAÇÃO: select_related múltiplo + filtro por usuário
        return ItemPedido.objects.select_related(
            'item',
            'item__categoria',  # Categoria do item
            'frota', 
            'pedido',
            'pedido__fornecedor',  # Fornecedor do pedido
            'criado_por'
        ).filter(
            criado_por=self.request.user
        ).order_by('-id')  # Usar -id em vez de -criado_em

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