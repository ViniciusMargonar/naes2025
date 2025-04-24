from django.urls import path

from .views import View1, View2, View3, etc #importar views CREATE aqui
from .views import View1, View2, View3, etc  # Importe views UPDATE aqui

urlpatterns = [
    #VIEWS CREATE
    path('cadastrar/view1/', View1.as_view(), name='view1-campus'),
    path('cadastrar/view2/', View2.as_view(), name='view2-curso'),
    path('cadastrar/view3/', View3.as_view(), name='view3-status'),
    # Adicione mais URLs conforme necessário

    #VIEW UPDATE
    path('editar/view1/<int:pk>/', View1.as_view(), name='view1-campus-update'),
    #localhost:8000/editar/view1/1/ (id=1) - Int:pk tem a função de pegar o id do objeto que queremos editar
    path('editar/view2/<int:pk>/', View2.as_view(), name='view2-curso-update'),
    path('editar/view3/<int:pk>/', View3.as_view(), name='view3-status-update'),
    # Adicione mais URLs conforme necessário
]
