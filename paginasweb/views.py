from django.shortcuts import render
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta

# View que apenas renderiza uma página Web
from django.views.generic import TemplateView

# Importar modelos para consultas
from cadastros.models import (
    Fornecedor, Frota, Item, Pedido, ItemPedido, CategoriaItem
)

# Create your views here.

# Cria uma view para renderizar a página inicial e faz uma herança de TemplateView
class PaginaInicial(TemplateView): 
    template_name = "paginasweb/modelos/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nome"] = "Vinícius Margonar"
        
        # Se o usuário estiver autenticado, buscar dados personalizados
        if self.request.user.is_authenticated:
            user = self.request.user
            
            # === CONSULTAS BÁSICAS DE CONTAGEM ===
            context['total_pedidos'] = Pedido.objects.filter(criado_por=user).count()
            context['total_fornecedores'] = Fornecedor.objects.filter(criado_por=user).count()
            context['total_frota'] = Frota.objects.filter(criado_por=user).count()
            context['total_itens'] = Item.objects.filter(criado_por=user).count()
            context['total_categorias'] = CategoriaItem.objects.filter(criado_por=user).count()
            
            # === CONSULTAS DE PEDIDOS ===
            # Pedidos por status
            context['pedidos_pendentes'] = Pedido.objects.filter(
                criado_por=user, 
                status='pendente'
            ).count()
            
            context['pedidos_em_andamento'] = Pedido.objects.filter(
                criado_por=user, 
                status='em_andamento'
            ).count()
            
            context['pedidos_entregues'] = Pedido.objects.filter(
                criado_por=user, 
                status='finalizado'
            ).count()
            
            # === ÚLTIMOS REGISTROS ===
            # Últimos 5 pedidos
            context['ultimos_pedidos'] = Pedido.objects.filter(
                criado_por=user
            ).select_related('fornecedor').order_by('-data_pedido')[:5]
            
            # Últimos 5 fornecedores (vou usar id para ordenação já que não tem campo de data)
            context['ultimos_fornecedores'] = Fornecedor.objects.filter(
                criado_por=user
            ).select_related('cidade', 'estado').order_by('-id')[:5]
            
            # Últimos 5 itens
            context['ultimos_itens'] = Item.objects.filter(
                criado_por=user
            ).select_related('categoria').order_by('-id')[:5]
            
            # === CONSULTAS AGREGADAS ===
            # ✅ OTIMIZAÇÃO: Valor total dos pedidos usando agregação SQL
            context['valor_total_pedidos'] = ItemPedido.objects.filter(
                criado_por=user
            ).aggregate(
                total=Sum('quantidade') * Sum('valor_unitario')
            ).get('total', 0) or 0
            
            # Quantidade total de itens pedidos
            context['quantidade_total_itens'] = ItemPedido.objects.filter(
                criado_por=user
            ).aggregate(
                total_quantidade=Sum('quantidade')
            ).get('total_quantidade', 0) or 0
            
            # === PEDIDOS PRÓXIMOS DO VENCIMENTO ===
            # Pedidos com entrega em até 7 dias
            data_limite = timezone.now().date() + timedelta(days=7)
            context['pedidos_urgentes'] = Pedido.objects.filter(
                criado_por=user,
                previsao_entrega__lte=data_limite,
                status__in=['pendente', 'em_andamento']
            ).select_related('fornecedor').order_by('previsao_entrega')[:5]
            
            # === ESTATÍSTICAS MENSAIS ===
            # Pedidos criados este mês
            inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            context['pedidos_este_mes'] = Pedido.objects.filter(
                criado_por=user,
                data_pedido__gte=inicio_mes
            ).count()
            
            # === FORNECEDORES MAIS UTILIZADOS ===
            # Top 5 fornecedores com mais pedidos
            context['top_fornecedores'] = Fornecedor.objects.filter(
                criado_por=user
            ).select_related('cidade', 'estado').annotate(
                num_pedidos=Count('pedido')
            ).filter(
                num_pedidos__gt=0
            ).order_by('-num_pedidos')[:5]
            
            # === ITENS MAIS PEDIDOS ===
            # Top 5 itens mais pedidos
            context['top_itens'] = Item.objects.filter(
                criado_por=user
            ).select_related('categoria').annotate(
                num_pedidos=Count('itempedido')
            ).filter(
                num_pedidos__gt=0
            ).order_by('-num_pedidos')[:5]
            
            # === VALOR TOTAL GASTO POR FORNECEDOR ===
            # ✅ OTIMIZAÇÃO: Usar agregação SQL em vez de loops Python
            from django.db.models import F
            
            fornecedores_valor = Fornecedor.objects.filter(
                criado_por=user
            ).select_related('cidade', 'estado').annotate(
                valor_total=Sum(
                    F('pedido__itempedido__quantidade') * F('pedido__itempedido__valor_unitario')
                )
            ).filter(
                valor_total__isnull=False,
                valor_total__gt=0
            ).order_by('-valor_total')[:5]
            
            # Formatação brasileira dos valores
            fornecedores_valor_formatados = []
            for fornecedor in fornecedores_valor:
                valor_total = fornecedor.valor_total or 0
                # Formatar valor para padrão brasileiro
                valor_formatado = "{:.2f}".format(valor_total)
                parts = valor_formatado.split('.')
                integer_part = parts[0]
                decimal_part = parts[1]
                
                # Adicionar pontos como separadores de milhares
                integer_reversed = integer_part[::-1]
                chunks = [integer_reversed[i:i+3] for i in range(0, len(integer_reversed), 3)]
                integer_formatted = '.'.join(chunks)[::-1]
                valor_br = f"{integer_formatted},{decimal_part}"
                
                fornecedores_valor_formatados.append({
                    'fornecedor': fornecedor,
                    'valor_total': valor_total,
                    'valor_formatado': valor_br
                })
            
            context['fornecedores_valor'] = fornecedores_valor_formatados
            
            # === FORNECEDORES COM PEDIDOS MAIS ATRASADOS ===
            # ✅ OTIMIZAÇÃO: Usar agregação SQL em vez de loops
            hoje = timezone.now().date()
            context['fornecedores_atrasados'] = Fornecedor.objects.filter(
                criado_por=user
            ).select_related('cidade', 'estado').annotate(
                pedidos_atrasados=Count(
                    'pedido',
                    filter=Q(
                        pedido__previsao_entrega__lt=hoje,
                        pedido__status__in=['pendente', 'em_andamento'],
                        pedido__criado_por=user
                    )
                )
            ).filter(
                pedidos_atrasados__gt=0
            ).order_by('-pedidos_atrasados')[:5]

        return context
    
class SobreView(TemplateView):
    template_name = "paginasweb/sobre.html"