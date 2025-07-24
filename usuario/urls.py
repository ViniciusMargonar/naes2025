from django.urls import path
from .views import login_user, logout_user, UsuarioCreate

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('cadastrar/', UsuarioCreate.as_view(), name='cadastrar-usuario'),
]