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
            # Valor total dos pedidos do usuário
            itens_pedido = ItemPedido.objects.filter(criado_por=user)
            valor_total = 0
            for item in itens_pedido:
                valor_total += (item.quantidade * item.valor_unitario) if item.quantidade and item.valor_unitario else 0
            context['valor_total_pedidos'] = valor_total
            
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
            ).order_by('previsao_entrega')[:5]
            
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
            ).annotate(
                num_pedidos=Count('pedido')
            ).filter(
                num_pedidos__gt=0
            ).order_by('-num_pedidos')[:5]
            
            # === ITENS MAIS PEDIDOS ===
            # Top 5 itens mais pedidos
            context['top_itens'] = Item.objects.filter(
                criado_por=user
            ).annotate(
                num_pedidos=Count('itempedido')
            ).filter(
                num_pedidos__gt=0
            ).order_by('-num_pedidos')[:5]
            
            # === VALOR TOTAL GASTO POR FORNECEDOR ===
            # Calcular valor total gasto por fornecedor
            fornecedores_valor = []
            for fornecedor in Fornecedor.objects.filter(criado_por=user):
                valor_total_fornecedor = 0
                pedidos_fornecedor = Pedido.objects.filter(
                    criado_por=user, 
                    fornecedor=fornecedor
                )
                for pedido in pedidos_fornecedor:
                    itens_pedido = ItemPedido.objects.filter(
                        criado_por=user,
                        pedido=pedido
                    )
                    for item in itens_pedido:
                        if item.quantidade and item.valor_unitario:
                            valor_total_fornecedor += (item.quantidade * item.valor_unitario)
                
                if valor_total_fornecedor > 0:
                    fornecedores_valor.append({
                        'fornecedor': fornecedor,
                        'valor_total': valor_total_fornecedor
                    })
            
            # Ordenar por valor total (maior para menor)
            fornecedores_valor.sort(key=lambda x: x['valor_total'], reverse=True)
            context['fornecedores_valor'] = fornecedores_valor[:5]  # Top 5
            
            # === FORNECEDORES COM PEDIDOS MAIS ATRASADOS ===
            # Fornecedores com pedidos atrasados (previsao_entrega já passou)
            hoje = timezone.now().date()
            fornecedores_atrasados = []
            
            for fornecedor in Fornecedor.objects.filter(criado_por=user):
                pedidos_atrasados = Pedido.objects.filter(
                    criado_por=user,
                    fornecedor=fornecedor,
                    previsao_entrega__lt=hoje,
                    status__in=['pendente', 'em_andamento']  # Não incluir pedidos já finalizados
                ).count()
                
                if pedidos_atrasados > 0:
                    fornecedores_atrasados.append({
                        'fornecedor': fornecedor,
                        'pedidos_atrasados': pedidos_atrasados
                    })
            
            # Ordenar por quantidade de pedidos atrasados (maior para menor)
            fornecedores_atrasados.sort(key=lambda x: x['pedidos_atrasados'], reverse=True)
            context['fornecedores_atrasados'] = fornecedores_atrasados[:5]  # Top 5

        return context
    
class SobreView(TemplateView):
    template_name = "paginasweb/sobre.html"