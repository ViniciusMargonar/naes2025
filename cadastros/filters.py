import django_filters
from django import forms
from .models import Pedido, Fornecedor, Item, Frota


class PedidoFilter(django_filters.FilterSet):
    # Filtro por nome do fornecedor (busca de texto)
    fornecedor__nome = django_filters.CharFilter(
        field_name='fornecedor__nome',
        lookup_expr='icontains',
        label='Nome do Fornecedor',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome do fornecedor...'
        })
    )
    
    # Mantém filtro por seleção de fornecedor também
    fornecedor = django_filters.ModelChoiceFilter(
        queryset=Fornecedor.objects.all(),
        label='Fornecedor (seleção)',
        empty_label='Selecione um fornecedor',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Filtro por status do pedido
    status = django_filters.ChoiceFilter(
        choices=Pedido.STATUS_CHOICES,
        label='Status do Pedido',
        empty_label='Todos os status',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Filtros de data do pedido (intervalo)
    data_pedido__gte = django_filters.DateFilter(
        field_name='data_pedido',
        lookup_expr='gte',
        label='Pedidos a partir de',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    data_pedido__lte = django_filters.DateFilter(
        field_name='data_pedido',
        lookup_expr='lte',
        label='Pedidos até',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    # Filtro por previsão de entrega
    previsao_entrega__gte = django_filters.DateFilter(
        field_name='previsao_entrega',
        lookup_expr='gte',
        label='Previsão a partir de',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    previsao_entrega__lte = django_filters.DateFilter(
        field_name='previsao_entrega',
        lookup_expr='lte',
        label='Previsão até',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    # Filtro por prefixo da frota (busca de texto)
    itempedido__frota__prefixo = django_filters.CharFilter(
        field_name='itempedido__frota__prefixo',
        lookup_expr='icontains',
        label='Prefixo da Frota',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 01-001, 05-002...'
        }),
        distinct=True
    )

    class Meta:
        model = Pedido
        fields = []  # Usar apenas os campos definidos explicitamente acima
        
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        
        # ✅ OTIMIZAÇÃO: Filtrar fornecedores por usuário com select_related
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            # Otimizar fornecedores com cidade e estado
            self.filters['fornecedor'].queryset = Fornecedor.objects.select_related(
                'cidade', 'estado'
            ).filter(
                criado_por=request.user
            ).order_by('nome')

