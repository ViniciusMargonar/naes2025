from django.urls import path

from .views import CategoriaItemCreate, CidadeCreate, EstadoCreate, FornecedorCreate, FrotaCreate, ItemCreate, ItemPedidoCreate, PedidoCreate, View1, View2, View3, etc #importar views CREATE aqui
from .views import View1, View2, View3, etc  # Importe views UPDATE aqui

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
    # Adicione mais URLs conforme necessário

    #VIEW UPDATE
    path('editar/view1/<int:pk>/', View1.as_view(), name='view1-campus-update'),
    #localhost:8000/editar/view1/1/ (id=1) - Int:pk tem a função de pegar o id do objeto que queremos editar
    path('editar/view2/<int:pk>/', View2.as_view(), name='view2-curso-update'),
    path('editar/view3/<int:pk>/', View3.as_view(), name='view3-status-update'),
    # Adicione mais URLs conforme necessário
]
