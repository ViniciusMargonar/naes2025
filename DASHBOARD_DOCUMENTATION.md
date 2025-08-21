# 📊 Dashboard Funcional AgroTrack - Documentação

## 🎯 Visão Geral

O dashboard da página inicial foi implementado com **QuerySets personalizados** e **consultas otimizadas** para fornecer informações relevantes e atualizadas em tempo real para cada usuário.

## 🔧 Funcionalidades Implementadas

### 1. **Estatísticas Básicas**
```python
# Contadores principais
- Total de Pedidos por usuário
- Total de Fornecedores cadastrados
- Total de Frota disponível
- Total de Itens no catálogo
- Pedidos criados este mês
```

### 2. **Análise de Status dos Pedidos**
```python
# Separação por status
- Pedidos Pendentes
- Pedidos Em Andamento
- Pedidos Finalizados (Entregues)
```

### 3. **Últimos Registros**
```python
# QuerySets com relacionamentos otimizados
- Últimos 5 pedidos (com select_related para fornecedor)
- Últimos 5 fornecedores (com cidade e estado)
- Últimos 5 itens (com categoria)
```

### 4. **Alertas de Urgência**
```python
# Pedidos próximos do vencimento
- Pedidos com entrega em até 7 dias
- Status: pendente ou em_andamento
- Ordenados por data de entrega mais próxima
```

### 5. **Rankings e Top Listas**
```python
# Consultas agregadas com COUNT
- Top 5 fornecedores mais utilizados
- Top 5 itens mais pedidos
- Baseado em relacionamentos e anotações
```

### 6. **Cálculos Financeiros**
```python
# Agregações de valores
- Valor total dos pedidos do usuário
- Quantidade total de itens pedidos
- Cálculos dinâmicos em tempo real
```

## 🏗️ Estrutura Técnica

### **View Principal (PaginaInicial)**
```python
class PaginaInicial(TemplateView):
    template_name = "paginasweb/modelos/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            user = self.request.user
            
            # === CONSULTAS OTIMIZADAS ===
            # Contadores básicos
            context['total_pedidos'] = Pedido.objects.filter(criado_por=user).count()
            
            # Últimos registros com select_related
            context['ultimos_pedidos'] = Pedido.objects.filter(
                criado_por=user
            ).select_related('fornecedor').order_by('-data_pedido')[:5]
            
            # Rankings com annotations
            context['top_fornecedores'] = Fornecedor.objects.filter(
                criado_por=user
            ).annotate(num_pedidos=Count('pedido')).order_by('-num_pedidos')[:5]
```

### **Consultas Personalizadas Destacadas**

#### 1. **Pedidos Urgentes**
```python
data_limite = timezone.now().date() + timedelta(days=7)
context['pedidos_urgentes'] = Pedido.objects.filter(
    criado_por=user,
    previsao_entrega__lte=data_limite,
    status__in=['pendente', 'em_andamento']
).order_by('previsao_entrega')[:5]
```

#### 2. **Estatísticas Mensais**
```python
inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
context['pedidos_este_mes'] = Pedido.objects.filter(
    criado_por=user,
    data_pedido__gte=inicio_mes
).count()
```

#### 3. **Top Fornecedores (Agregação)**
```python
context['top_fornecedores'] = Fornecedor.objects.filter(
    criado_por=user
).annotate(
    num_pedidos=Count('pedido')
).filter(
    num_pedidos__gt=0
).order_by('-num_pedidos')[:5]
```

## 🎨 Interface do Dashboard

### **Seção 1: Cards de Estatísticas**
- **4 Cards principais** com ícones e cores diferenciadas
- **Números dinâmicos** atualizados em tempo real
- **Informações complementares** (ex: "X este mês")
- **Links diretos** para listagens completas

### **Seção 2: Status dos Pedidos**
- **3 Cards de status** com cores semafóricas
- **Pendentes** (vermelho) - urgência
- **Em Andamento** (amarelo) - atenção
- **Finalizados** (verde) - sucesso

### **Seção 3: Últimos Registros e Alertas**
- **Card de Últimos Pedidos** com informações detalhadas
- **Card de Pedidos Urgentes** com alertas visuais
- **Card de Top Fornecedores** com rankings
- **Card de Top Itens** com estatísticas de uso

## 📱 Responsividade

```css
/* Mobile-first design */
@media (max-width: 768px) {
    .dashboard-card {
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .dashboard-number {
        font-size: 2rem;
    }
}
```

## 🔐 Segurança e Acesso

- **Controle por usuário**: Cada usuário vê apenas seus dados
- **QuerySets filtrados**: Todas as consultas incluem `criado_por=user`
- **Validação de autenticação**: Dashboard só aparece para usuários logados

## 📈 Performance

### **Otimizações Implementadas**
1. **select_related()** para relacionamentos FK
2. **Annotations** para cálculos agregados
3. **Limitação de resultados** com slice [:5]
4. **Índices nos campos** de busca frequente

### **QuerySets Eficientes**
```python
# Em vez de múltiplas consultas
# pedido.fornecedor.nome (causa N+1 queries)

# Usamos select_related
Pedido.objects.filter(criado_por=user).select_related('fornecedor')
```

## 🎯 Benefícios para o Usuário

1. **Visão Geral Instantânea** - Números principais em destaque
2. **Alertas Proativos** - Pedidos urgentes em evidência
3. **Análise de Tendências** - Top fornecedores e itens
4. **Acesso Rápido** - Links diretos para ações
5. **Dados Personalizados** - Informações específicas do usuário
6. **Interface Intuitiva** - Design responsivo e moderno

## 🔄 Como Testar

1. **Faça login** com `usuario1` (senha: `senha123`)
2. **Navegue pela página inicial** - veja os dados populados
3. **Verifique os números** - devem corresponder aos dados reais
4. **Clique nos links** - navegação para listagens completas
5. **Teste com `usuario2`** - dados isolados por usuário

## 🛠️ Comando de Dados de Teste

```bash
python manage.py criar_dados_teste
```

Este comando cria:
- **10 pedidos** com datas variadas
- **3 fornecedores** diferentes
- **7 itens** em 5 categorias
- **3 veículos** na frota
- **Dados separados** por usuário para teste de isolamento

---

✅ **Dashboard Totalmente Funcional e Otimizado!**
