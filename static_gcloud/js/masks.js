// Máscaras de formatação para formulários

document.addEventListener('DOMContentLoaded', function() {
    
    // Função para aplicar máscara CNPJ
    function applyCnpjMask(value) {
        // Remove tudo que não é dígito
        value = value.replace(/\D/g, '');
        
        // Limita a 14 dígitos
        value = value.substring(0, 14);
        
        // Aplica a máscara progressivamente
        if (value.length <= 2) {
            return value;
        } else if (value.length <= 5) {
            return value.replace(/(\d{2})(\d+)/, '$1.$2');
        } else if (value.length <= 8) {
            return value.replace(/(\d{2})(\d{3})(\d+)/, '$1.$2.$3');
        } else if (value.length <= 12) {
            return value.replace(/(\d{2})(\d{3})(\d{3})(\d+)/, '$1.$2.$3/$4');
        } else {
            return value.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d+)/, '$1.$2.$3/$4-$5');
        }
    }

    // Função para aplicar máscara de Telefone
    function applyPhoneMask(value) {
        // Remove tudo que não é dígito
        value = value.replace(/\D/g, '');
        
        // Limita a 11 dígitos (DDD + 9 dígitos)
        value = value.substring(0, 11);
        
        // Aplica a máscara progressivamente
        if (value.length <= 2) {
            return value;
        } else if (value.length <= 7) {
            return value.replace(/(\d{2})(\d+)/, '($1) $2');
        } else if (value.length <= 11) {
            return value.replace(/(\d{2})(\d{5})(\d+)/, '($1) $2-$3');
        }
        
        return value;
    }

    // Aplicar máscara CNPJ ao campo
    const cnpjField = document.getElementById('id_cnpj');
    if (cnpjField) {
        // Definir atributos do campo
        cnpjField.maxLength = 18;
        cnpjField.placeholder = '99.999.999/9999-99';
        
        cnpjField.addEventListener('input', function(e) {
            const cursorPosition = e.target.selectionStart;
            const oldValue = e.target.value;
            const newValue = applyCnpjMask(e.target.value);
            
            // Atualiza o valor
            e.target.value = newValue;
            
            // Calcula a nova posição do cursor
            let newCursorPosition = cursorPosition;
            if (newValue.length > oldValue.length) {
                // Se caracteres foram adicionados (pontos, barras, hífens)
                const addedChars = newValue.length - oldValue.length;
                newCursorPosition = Math.min(cursorPosition + addedChars, newValue.length);
            }
            
            // Reposiciona o cursor
            e.target.setSelectionRange(newCursorPosition, newCursorPosition);
        });

        // Também aplicar máscara ao colar
        cnpjField.addEventListener('paste', function(e) {
            setTimeout(() => {
                e.target.value = applyCnpjMask(e.target.value);
            }, 10);
        });

        // Aplicar máscara no valor inicial se houver
        if (cnpjField.value) {
            cnpjField.value = applyCnpjMask(cnpjField.value);
        }
    }

    // Aplicar máscara de Telefone ao campo
    const phoneField = document.getElementById('id_telefone');
    if (phoneField) {
        // Definir atributos do campo
        phoneField.maxLength = 15;
        phoneField.placeholder = '(11) 99999-9999';
        
        phoneField.addEventListener('input', function(e) {
            const cursorPosition = e.target.selectionStart;
            const oldValue = e.target.value;
            const newValue = applyPhoneMask(e.target.value);
            
            // Atualiza o valor
            e.target.value = newValue;
            
            // Calcula a nova posição do cursor
            let newCursorPosition = cursorPosition;
            if (newValue.length > oldValue.length) {
                // Se caracteres foram adicionados (parênteses, espaços, hífens)
                const addedChars = newValue.length - oldValue.length;
                newCursorPosition = Math.min(cursorPosition + addedChars, newValue.length);
            }
            
            // Reposiciona o cursor
            e.target.setSelectionRange(newCursorPosition, newCursorPosition);
        });

        // Também aplicar máscara ao colar
        phoneField.addEventListener('paste', function(e) {
            setTimeout(() => {
                e.target.value = applyPhoneMask(e.target.value);
            }, 10);
        });

        // Aplicar máscara no valor inicial se houver
        if (phoneField.value) {
            phoneField.value = applyPhoneMask(phoneField.value);
        }
    }
});
