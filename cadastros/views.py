from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django_filters.views import FilterView
from .models import (
    Estado, Cidade, Fornecedor, Frota,
    CategoriaItem, Item, ItemPedido, Pedido, MovimentacaoPedido
)
from .forms import PedidoComItensForm
from .filters import PedidoFilter


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


class PedidoCreate(LoginRequiredMixin, View):
    template_name = 'cadastros/pedido_form.html'
    
    def get(self, request):
        form_wrapper = PedidoComItensForm(user=request.user)
        
        context = {
            'titulo': 'Cadastrar Pedido',
            'pedido_form': form_wrapper.pedido_form,
            'item_formset': form_wrapper.item_formset,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form_wrapper = PedidoComItensForm(data=request.POST, user=request.user)

        if form_wrapper.is_valid():
            try:
                pedido = form_wrapper.save()

                MovimentacaoPedido.objects.create(
                    pedido=pedido,
                    tipo='criacao',
                    status_novo=pedido.status,
                    observacao=f'Pedido criado com {pedido.itempedido_set.count()} itens. Valor total: R$ {pedido.valor_total}',
                    usuario=request.user
                )

                messages.success(request, f'Pedido #{pedido.id} criado com sucesso!')
                return redirect('pedido-list')
            except Exception as e:
                messages.error(request, f'Erro ao criar pedido: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')

        context = {
            'titulo': 'Cadastrar Pedido',
            'pedido_form': form_wrapper.pedido_form,
            'item_formset': form_wrapper.item_formset,
        }
        return render(request, self.template_name, context)

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


class PedidoUpdate(LoginRequiredMixin, OwnerRequiredMixin, View):
    template_name = 'cadastros/pedido_form.html'
    
    def get(self, request, pk):
        try:
            pedido = Pedido.objects.select_related(
                'fornecedor',
                'fornecedor__cidade',
                'fornecedor__estado',
                'criado_por'
            ).prefetch_related(
                'itempedido_set__item',
                'itempedido_set__item__categoria',
                'itempedido_set__frota'
            ).get(pk=pk, criado_por=request.user)
        except Pedido.DoesNotExist:
            messages.error(request, 'Pedido não encontrado.')
            return redirect('pedido-list')
        
        form_wrapper = PedidoComItensForm(instance=pedido, user=request.user)
        
        context = {
            'titulo': f'Editar Pedido #{pedido.id}',
            'pedido_form': form_wrapper.pedido_form,
            'item_formset': form_wrapper.item_formset,
            'pedido': pedido,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        try:
            pedido = Pedido.objects.select_related(
                'fornecedor',
                'criado_por'
            ).get(pk=pk, criado_por=request.user)
        except Pedido.DoesNotExist:
            messages.error(request, 'Pedido não encontrado.')
            return redirect('pedido-list')

        status_anterior = pedido.status

        form_wrapper = PedidoComItensForm(data=request.POST, instance=pedido, user=request.user)

        if form_wrapper.is_valid():
            try:
                pedido_atualizado = form_wrapper.save()

                if status_anterior != pedido_atualizado.status:
                    MovimentacaoPedido.objects.create(
                        pedido=pedido_atualizado,
                        tipo='alteracao_status',
                        status_anterior=status_anterior,
                        status_novo=pedido_atualizado.status,
                        observacao=f'Status alterado de "{pedido_atualizado.get_status_display()}" para "{dict(Pedido.STATUS_CHOICES).get(pedido_atualizado.status)}"',
                        usuario=request.user
                    )
                else:
                    MovimentacaoPedido.objects.create(
                        pedido=pedido_atualizado,
                        tipo='alteracao_dados',
                        status_anterior=status_anterior,
                        status_novo=pedido_atualizado.status,
                        observacao=f'Dados do pedido atualizados. Valor total: R$ {pedido_atualizado.valor_total}',
                        usuario=request.user
                    )

                messages.success(request, f'Pedido #{pedido_atualizado.id} atualizado com sucesso!')
                return redirect('pedido-list')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar pedido: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
        
        try:
            pedido = Pedido.objects.select_related(
                'fornecedor',
                'fornecedor__cidade',
                'fornecedor__estado',
                'criado_por'
            ).prefetch_related(
                'itempedido_set__item',
                'itempedido_set__item__categoria',
                'itempedido_set__frota'
            ).get(pk=pk, criado_por=request.user)
        except Pedido.DoesNotExist:
            messages.error(request, 'Pedido não encontrado.')
            return redirect('pedido-list')
        
        context = {
            'titulo': f'Editar Pedido #{pedido.id}',
            'pedido_form': form_wrapper.pedido_form,
            'item_formset': form_wrapper.item_formset,
            'pedido': pedido,
        }
        return render(request, self.template_name, context)


class ItemPedidoUpdate(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'cadastros/form.html'
    model = ItemPedido
    success_url = reverse_lazy('itempedido-list')
    fields = ['item', 'frota', 'pedido', 'status', 'quantidade', 'valor_unitario']
    extra_context = {'titulo': 'Atualizar Item do Pedido'}
    success_message = "Item do pedido atualizado com sucesso!"


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


class EstadoList(LoginRequiredMixin, ListView):
    template_name = 'listas/estado.html'
    model = Estado
    context_object_name = 'estados'
    paginate_by = 20

    def get_queryset(self):
        return Estado.objects.all().order_by('nome')


class CidadeList(LoginRequiredMixin, ListView):
    template_name = 'listas/cidade.html'
    model = Cidade
    context_object_name = 'cidades'
    paginate_by = 20

    def get_queryset(self):
        return Cidade.objects.select_related('estado').order_by('nome')


class FornecedorList(LoginRequiredMixin, ListView):
    template_name = 'listas/fornecedor.html'
    model = Fornecedor
    context_object_name = 'fornecedores'
    paginate_by = 20

    def get_queryset(self):
        return Fornecedor.objects.select_related(
            'cidade',
            'cidade__estado',
            'estado',
            'criado_por'
        ).filter(
            criado_por=self.request.user
        ).order_by('-id')


class FrotaList(LoginRequiredMixin, ListView):
    template_name = 'listas/frota.html'
    model = Frota
    context_object_name = 'frotas'
    paginate_by = 20

    def get_queryset(self):
        return Frota.objects.select_related('criado_por').filter(
            criado_por=self.request.user
        ).order_by('-id')


class CategoriaItemList(LoginRequiredMixin, ListView):
    template_name = 'listas/categoriaitem.html'
    model = CategoriaItem
    context_object_name = 'categorias'
    paginate_by = 20

    def get_queryset(self):
        return CategoriaItem.objects.select_related('criado_por').filter(
            criado_por=self.request.user
        ).order_by('nome')


class ItemList(LoginRequiredMixin, ListView):
    template_name = 'listas/item.html'
    model = Item
    context_object_name = 'itens'
    paginate_by = 20

    def get_queryset(self):
        return Item.objects.select_related(
            'categoria',
            'criado_por'
        ).filter(
            criado_por=self.request.user
        ).order_by('nome')


class PedidoList(LoginRequiredMixin, FilterView):
    template_name = 'listas/pedido.html'
    model = Pedido
    context_object_name = 'pedidos'
    filterset_class = PedidoFilter
    paginate_by = 20

    def get_queryset(self):
        return Pedido.objects.select_related(
            'fornecedor',
            'fornecedor__cidade',
            'criado_por'
        ).prefetch_related(
            'itempedido_set__item',
            'itempedido_set__item__categoria',
            'itempedido_set__frota'
        ).filter(
            criado_por=self.request.user
        ).order_by('-data_pedido')

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtered_queryset = context['filter'].qs

        context['total_filtrado'] = filtered_queryset.count()
        context['total_geral'] = self.get_queryset().count()
        context['stats_status'] = {
            'pendente': filtered_queryset.filter(status='pendente').count(),
            'em_andamento': filtered_queryset.filter(status='em_andamento').count(),
            'finalizado': filtered_queryset.filter(status='finalizado').count(),
        }

        return context


class ItemPedidoList(LoginRequiredMixin, ListView):
    template_name = 'listas/itempedido.html'
    model = ItemPedido
    context_object_name = 'itens_pedido'
    paginate_by = 20

    def get_queryset(self):
        return ItemPedido.objects.select_related(
            'item',
            'item__categoria',
            'frota',
            'pedido',
            'pedido__fornecedor',
            'criado_por'
        ).filter(
            criado_por=self.request.user
        ).order_by('-id')