from django.urls import path
# Importar suas Views
from .views import PaginaInicial

urlpatterns = [
    path("", PaginaInicial.as_view(), name="index"),
]