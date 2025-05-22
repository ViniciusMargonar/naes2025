from django.urls import path

from .views import CategoriaItemCreate, CidadeCreate, EstadoCreate, FornecedorCreate, FrotaCreate, ItemCreate, ItemPedidoCreate, PedidoCreate
from .views import EstadoUpdate, CidadeUpdate, FornecedorUpdate, FrotaUpdate, CategoriaItemUpdate, ItemUpdate, PedidoUpdate, ItemPedidoUpdate
from .views import EstadoList, CidadeList, FornecedorList, FrotaList, CategoriaItemList, ItemList, PedidoList, ItemPedidoList
#Importar aqui TAMBÉM as views para LIST


urlpatterns = [
    #VIEWS CREATE
    path('cadastrar/estado/', EstadoCreate.as_view(), name='cadastrar-estado'),
    path('cadastrar/cidade/', CidadeCreate.as_view(), name='cadastrar-cidade'),
    path('cadastrar/fornecedor/', FornecedorCreate.as_view(), name='cadastrar-fornecedor'),
    path('cadastrar/frota/', FrotaCreate.as_view(), name='cadastrar-frota'),
    path('cadastrar/categoriaitem/', CategoriaItemCreate.as_view(), name='cadastrar-categoriaitem'),
    path('cadastrar/item/', ItemCreate.as_view(), name='cadastrar-item'),
    path('cadastrar/itempedido/', ItemPedidoCreate.as_view(), name='cadastrar-itempedido'),
    path('cadastrar/pedido/', PedidoCreate.as_view(), name='cadastrar-pedido'),

    #VIEWS UPDATE
    path('editar/estado/<int:pk>/', EstadoUpdate.as_view(), name='estado-update'),
    path('editar/cidade/<int:pk>/', CidadeUpdate.as_view(), name='cidade-update'),
    path('editar/fornecedor/<int:pk>/', FornecedorUpdate.as_view(), name='fornecedor-update'),
    path('editar/frota/<int:pk>/', FrotaUpdate.as_view(), name='frota-update'),
    path('editar/categoriaitem/<int:pk>/', CategoriaItemUpdate.as_view(), name='categoriaitem-update'),
    path('editar/item/<int:pk>/', ItemUpdate.as_view(), name='item-update'),
    path('editar/pedido/<int:pk>/', PedidoUpdate.as_view(), name='pedido-update'),
    path('editar/itempedido/<int:pk>/', ItemPedidoUpdate.as_view(), name='itempedido-update'),

    #VIEWS LIST
    path('listar/estado/', EstadoList.as_view(), name='estado-list'),
    path('listar/cidade/', CidadeList.as_view(), name='cidade-list'),
    path('listar/fornecedor/', FornecedorList.as_view(), name='fornecedor-list'),
    path('listar/frota/', FrotaList.as_view(), name='frota-list'),
    path('listar/categoriaitem/', CategoriaItemList.as_view(), name='categoriaitem-list'),
    path('listar/item/', ItemList.as_view(), name='item-list'),
    path('listar/pedido/', PedidoList.as_view(), name='pedido-list'),
    path('listar/itempedido/', ItemPedidoList.as_view(), name='itempedido-list'),
    
    #localhost:8000/editar/view1/1/ (id=1) - Int:pk tem a função de pegar o id do objeto que queremos editar
]
