from django.urls import path

from .views import View1, View2, View3, etc

urlpatterns = [
    path('view1/campus/', View1.as_view(), name='view1-campus'),
    path('view2/curso/', View2.as_view(), name='view2-curso'),
    path('view3/status/', View3.as_view(), name='view3-status'),
    # Adicione mais URLs conforme necessário
]
