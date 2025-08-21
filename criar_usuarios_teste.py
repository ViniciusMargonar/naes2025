#!/usr/bin/env python
"""
Script para criar usuários de teste para validar o sistema de controle de acesso.
"""

import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'naes2025.settings')
django.setup()

from django.contrib.auth.models import User, Group

def criar_usuarios_teste():
    """Cria dois usuários de teste para validar o controle de acesso."""
    
    # Verificar se os grupos existem
    try:
        grupo_usuario = Group.objects.get(name='Usuario')
        print("X Grupo 'Usuario' encontrado")
    except Group.DoesNotExist:
        print("X Grupo 'Usuario' nao encontrado. Execute: python manage.py criar_grupos")
        return
    
    # Criar primeiro usuário
    usuario1, created1 = User.objects.get_or_create(
        username='usuario1',
        defaults={
            'email': 'usuario1@teste.com',
            'first_name': 'Usuário',
            'last_name': 'Um'
        }
    )
    
    if created1:
        usuario1.set_password('senha123')
        usuario1.save()
        usuario1.groups.add(grupo_usuario)
        print("X Usuario 'usuario1' criado com sucesso")
    else:
        print("! Usuario 'usuario1' ja existe")
    
    # Criar segundo usuário
    usuario2, created2 = User.objects.get_or_create(
        username='usuario2',
        defaults={
            'email': 'usuario2@teste.com',
            'first_name': 'Usuário',
            'last_name': 'Dois'
        }
    )
    
    if created2:
        usuario2.set_password('senha123')
        usuario2.save()
        usuario2.groups.add(grupo_usuario)
        print("X Usuario 'usuario2' criado com sucesso")
    else:
        print("! Usuario 'usuario2' ja existe")
    
    print("\nINSTRUCOES PARA TESTE:")
    print("1. Acesse http://127.0.0.1:8000/usuario/login/")
    print("2. Faca login com 'usuario1' (senha: senha123)")
    print("3. Cadastre alguns registros (fornecedores, itens, etc.)")
    print("4. Faca logout e login com 'usuario2' (senha: senha123)")
    print("5. Tente editar/excluir os registros do usuario1")
    print("6. Voce deve receber erro 403 (Acesso Negado)")
    print("\nCONTROLE DE ACESSO:")
    print("- Cada usuario so pode editar/excluir seus proprios registros")
    print("- Todos podem visualizar listas gerais")
    print("- Apenas o criador do registro tem acesso as acoes de modificacao")

if __name__ == '__main__':
    criar_usuarios_teste()
