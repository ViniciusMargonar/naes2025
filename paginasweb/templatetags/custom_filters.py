from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def br_currency(value):
    """
    Formata um valor para o padrão monetário brasileiro
    Exemplo: 1234.56 -> 1.234,56
    """
    try:
        # Converte para float se for string
        if isinstance(value, str):
            value = float(value)
        
        # Formata com 2 casas decimais
        formatted = "{:.2f}".format(float(value))
        
        # Separa parte inteira e decimal
        parts = formatted.split('.')
        integer_part = parts[0]
        decimal_part = parts[1]
        
        # Adiciona pontos como separadores de milhares
        # Inverte a string, adiciona pontos a cada 3 dígitos e inverte novamente
        integer_reversed = integer_part[::-1]
        chunks = [integer_reversed[i:i+3] for i in range(0, len(integer_reversed), 3)]
        integer_formatted = '.'.join(chunks)[::-1]
        
        # Junta parte inteira formatada com vírgula e decimais
        result = f"{integer_formatted},{decimal_part}"
        
        return mark_safe(result)
    except (ValueError, TypeError):
        return value
