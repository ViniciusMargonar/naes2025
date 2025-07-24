from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from cadastros.models import Fornecedor, Estado, Cidade, Frota, Item, Pedido


class Command(BaseCommand):
    help = 'Cria grupos de usuários e define permissões'

    def handle(self, *args, **options):
        # Criar grupos
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        usuario_group, created = Group.objects.get_or_create(name='Usuarios')
        
        # Permissões para Administradores (todas)
        admin_permissions = Permission.objects.all()
        admin_group.permissions.set(admin_permissions)
        
        # Permissões para Usuários (apenas visualizar e adicionar)
        usuario_permissions = []
        models = [Fornecedor, Estado, Cidade, Frota, Item, Pedido]
        
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            view_perm = Permission.objects.get(
                codename=f'view_{model._meta.model_name}',
                content_type=content_type
            )
            add_perm = Permission.objects.get(
                codename=f'add_{model._meta.model_name}',
                content_type=content_type
            )
            usuario_permissions.extend([view_perm, add_perm])
        
        usuario_group.permissions.set(usuario_permissions)
        
        self.stdout.write(
            self.style.SUCCESS(
                'Grupos criados com sucesso:\n'
                '- Administradores: Todas as permissões\n'
                '- Usuarios: Visualizar e adicionar registros'
            )
        )
