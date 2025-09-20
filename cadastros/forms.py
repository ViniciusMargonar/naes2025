from django import forms
from django.forms import inlineformset_factory
from .models import Pedido, ItemPedido, Fornecedor, Item, Frota


class PedidoForm(forms.ModelForm):
    previsao_entrega = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        input_formats=['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'],
        label='Previsão de Entrega'
    )
    
    class Meta:
        model = Pedido
        fields = ['fornecedor', 'descricao', 'previsao_entrega', 'status']
        widgets = {
            'fornecedor': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_fornecedor'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva detalhes sobre o pedido...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_status'
            }),
        }
        labels = {
            'fornecedor': 'Fornecedor',
            'descricao': 'Descrição/Observações',
            'status': 'Status do Pedido',
        }


class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['item', 'quantidade', 'valor_unitario', 'frota']
        widgets = {
            'item': forms.Select(attrs={
                'class': 'form-select item-select',
                'required': True
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'valor_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'frota': forms.Select(attrs={
                'class': 'form-select',
                'required': False
            }),
        }
        labels = {
            'item': 'Item',
            'quantidade': 'Quantidade',
            'valor_unitario': 'Valor Unitário (R$)',
            'frota': 'Frota (Opcional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar opção vazia para frota
        self.fields['frota'].empty_label = "Selecione uma frota (opcional)"
        self.fields['item'].empty_label = "Selecione um item"


# Formset para múltiplos itens
ItemPedidoFormSet = inlineformset_factory(
    Pedido, 
    ItemPedido,
    form=ItemPedidoForm,
    extra=0,  # Não começar com nenhum formulário
    min_num=1,  # Pelo menos 1 item é obrigatório
    validate_min=True,
    can_delete=True,
    fields=['item', 'quantidade', 'valor_unitario', 'frota']
)


class PedidoComItensForm:
    """
    Classe wrapper para gerenciar o formulário do pedido junto com os itens
    """
    
    def __init__(self, data=None, instance=None, user=None):
        self.user = user
        self.instance = instance
        
        # Se é edição, incluir o campo status
        if instance:
            self.pedido_form = PedidoForm(data=data, instance=instance)
        else:
            # Para criação, usar formulário sem status
            class PedidoCreateForm(forms.ModelForm):
                previsao_entrega = forms.DateField(
                    required=False,
                    widget=forms.DateInput(attrs={
                        'class': 'form-control',
                        'type': 'date'
                    }),
                    input_formats=['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'],
                    label='Previsão de Entrega'
                )
                
                class Meta:
                    model = Pedido
                    fields = ['fornecedor', 'descricao', 'previsao_entrega']
                    widgets = {
                        'fornecedor': forms.Select(attrs={
                            'class': 'form-select',
                            'id': 'id_fornecedor'
                        }),
                        'descricao': forms.Textarea(attrs={
                            'class': 'form-control',
                            'rows': 3,
                            'placeholder': 'Descreva detalhes sobre o pedido...'
                        }),
                    }
                    labels = {
                        'fornecedor': 'Fornecedor',
                        'descricao': 'Descrição/Observações',
                    }
            
            self.pedido_form = PedidoCreateForm(data=data)
            
        self.item_formset = ItemPedidoFormSet(
            data=data, 
            instance=instance,
            prefix='itens'
        )
        
        # ✅ OTIMIZAÇÃO: Filtrar fornecedores e itens por usuário com select_related
        if user:
            # Otimizar query para fornecedores com cidade e estado
            self.pedido_form.fields['fornecedor'].queryset = Fornecedor.objects.select_related(
                'cidade', 'estado'
            ).filter(criado_por=user).order_by('nome')
            
            # ✅ OTIMIZAÇÃO: Aplicar filtros otimizados para cada formulário no formset
            for form in self.item_formset:
                # Otimizar query para itens com categoria
                form.fields['item'].queryset = Item.objects.select_related(
                    'categoria'
                ).filter(criado_por=user).order_by('nome')
                
                # Otimizar query para frotas
                form.fields['frota'].queryset = Frota.objects.filter(
                    criado_por=user
                ).order_by('prefixo')
    
    def is_valid(self):
        return self.pedido_form.is_valid() and self.item_formset.is_valid()
    
    def save(self, commit=True):
        # Salvar o pedido primeiro
        pedido = self.pedido_form.save(commit=False)
        if self.user:
            pedido.criado_por = self.user
        
        if commit:
            pedido.save()
            
            # Salvar os itens do pedido
            self.item_formset.instance = pedido
            itens_modificados = self.item_formset.save(commit=False)
            
            # Salvar itens modificados
            for item in itens_modificados:
                item.criado_por = self.user
                item.save()
            
            # Processar itens marcados para deletar
            for item in self.item_formset.deleted_objects:
                item.delete()
            
            # ✅ CORREÇÃO: Recalcular valor total com TODOS os itens do pedido
            # (não apenas os modificados)
            valor_total = 0
            for item_pedido in pedido.itempedido_set.all():
                valor_total += item_pedido.quantidade * item_pedido.valor_unitario
            
            # Atualizar valor total do pedido
            pedido.valor_total = valor_total
            pedido.save()
            
        return pedido
    
    @property
    def errors(self):
        errors = {}
        if self.pedido_form.errors:
            errors['pedido'] = self.pedido_form.errors
        if self.item_formset.errors:
            errors['itens'] = self.item_formset.errors
        return errors