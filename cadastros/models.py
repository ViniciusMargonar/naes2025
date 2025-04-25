from django.db import models
from django.contrib.auth.models import User

class Estado(models.Model):
    SIGLA_ESTADOS_BRASILEIROS = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ]

    nome = models.CharField(max_length=100,choices=SIGLA_ESTADOS_BRASILEIROS)
    sigla = models.CharField(max_length=2, choices=SIGLA_ESTADOS_BRASILEIROS)

    def __str__(self):
        return self.sigla

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ['nome']



class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} - {self.estado.sigla}"

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
        ordering = ['nome']


class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome']


class Frota(models.Model):
    prefixo = models.CharField(max_length=10)
    descricao = models.CharField(max_length=255)
    ano = models.PositiveIntegerField()
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Frota {self.prefixo} - {self.ano}"

    class Meta:
        verbose_name = "Frota"
        verbose_name_plural = "Frotas"
        ordering = ['prefixo']


class CategoriaItem(models.Model):
    nome = models.CharField(max_length=100)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria de Item"
        verbose_name_plural = "Categorias de Itens"
        ordering = ['nome']


class Item(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey('CategoriaItem', on_delete=models.CASCADE)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Itens"
        ordering = ['nome']


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
    ]

    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    descricao = models.TextField()
    data_pedido = models.DateTimeField(auto_now_add=True)
    previsao_entrega = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Pedido #{self.id} - {self.fornecedor}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_pedido']


class ItemPedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
        ('entregue', 'Entregue'),
    ]

    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    frota = models.ForeignKey('Frota', on_delete=models.SET_NULL, null=True, blank=True)
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    quantidade = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantidade}x {self.item.nome} para Pedido #{self.pedido.id}"

    class Meta:
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Itens de Pedido"
        ordering = ['pedido', 'item']
