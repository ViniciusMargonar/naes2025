from django.contrib import admin
from .models import (
    Estado, Cidade, Fornecedor, Frota,
    CategoriaItem, Item, Pedido, ItemPedido
)

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla')
    search_fields = ('nome', 'sigla')


@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado')
    list_filter = ('estado',)
    search_fields = ('nome',)


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'cidade', 'criado_por')
    list_filter = ('cidade',)
    search_fields = ('nome', 'cnpj')


@admin.register(Frota)
class FrotaAdmin(admin.ModelAdmin):
    list_display = ('prefixo', 'descricao', 'ano', 'criado_por')
    search_fields = ('prefixo', 'descricao')


@admin.register(CategoriaItem)
class CategoriaItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_por')
    search_fields = ('nome',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'criado_por')
    list_filter = ('categoria',)
    search_fields = ('nome',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fornecedor', 'data_pedido', 'status', 'criado_por', 'valor_total')
    list_filter = ('status', 'data_pedido', 'fornecedor')
    search_fields = ('descricao',)


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('item', 'pedido', 'frota', 'status', 'quantidade', 'valor_unitario', 'criado_por')
    list_filter = ('status', 'pedido', 'item')
    search_fields = ('item__nome', 'pedido__id')
