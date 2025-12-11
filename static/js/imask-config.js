/**
 * Configuração centralizada do IMask.js para máscaras de input
 * AgroTrack - Sistema de Gestão de Pedidos
 */

document.addEventListener('DOMContentLoaded', function() {

    // ============================================
    // MÁSCARA: CNPJ (99.999.999/9999-99)
    // ============================================
    const cnpjFields = document.querySelectorAll('#id_cnpj, input[name*="cnpj"]');
    cnpjFields.forEach(function(field) {
        IMask(field, {
            mask: '00.000.000/0000-00',
            lazy: false,  // Mostra a máscara mesmo quando vazio
            placeholderChar: '_'
        });

        // Adicionar placeholder visual
        field.placeholder = '99.999.999/9999-99';
    });

    // ============================================
    // MÁSCARA: TELEFONE ((99) 99999-9999)
    // ============================================
    const telefoneFields = document.querySelectorAll('#id_telefone, input[name*="telefone"]');
    telefoneFields.forEach(function(field) {
        IMask(field, {
            mask: [
                {
                    // Telefone fixo: (99) 9999-9999
                    mask: '(00) 0000-0000'
                },
                {
                    // Celular: (99) 99999-9999
                    mask: '(00) 00000-0000'
                }
            ],
            lazy: false,
            placeholderChar: '_'
        });

        field.placeholder = '(99) 99999-9999';
    });

    // ============================================
    // MÁSCARA: MOEDA (R$ 9.999,99)
    // ============================================
    const moedaFields = document.querySelectorAll(
        'input[name*="valor"], ' +
        'input[name*="preco"], ' +
        'input[name*="valor_unitario"], ' +
        'input[type="number"][step="0.01"]'
    );

    moedaFields.forEach(function(field) {
        // Salvar valor original se existir
        const valorOriginal = field.value;

        const maskInstance = IMask(field, {
            mask: 'R$ num',
            blocks: {
                num: {
                    mask: Number,
                    thousandsSeparator: '.',  // Separador de milhar
                    radix: ',',                // Separador decimal
                    scale: 2,                  // Casas decimais
                    min: 0,                    // Valor mínimo
                    max: 999999999.99,         // Valor máximo
                    padFractionalZeros: true,  // Preenche com zeros (ex: 10,00)
                    normalizeZeros: true,      // Remove zeros à esquerda
                    mapToRadix: ['.']          // Aceita ponto como vírgula
                }
            }
        });

        // Restaurar valor original formatado
        if (valorOriginal) {
            const valorNumerico = parseFloat(valorOriginal.replace(',', '.'));
            if (!isNaN(valorNumerico)) {
                maskInstance.value = valorNumerico.toString();
            }
        }

        // Remover o atributo type="number" para evitar conflitos
        if (field.type === 'number') {
            field.type = 'text';
        }

        // Adicionar classe para identificar campos com máscara de moeda
        field.classList.add('masked-currency');
    });

    // ============================================
    // MÁSCARA: CPF (999.999.999-99)
    // ============================================
    const cpfFields = document.querySelectorAll('#id_cpf, input[name*="cpf"]');
    cpfFields.forEach(function(field) {
        IMask(field, {
            mask: '000.000.000-00',
            lazy: false,
            placeholderChar: '_'
        });

        field.placeholder = '999.999.999-99';
    });

    // ============================================
    // MÁSCARA: CEP (99999-999)
    // ============================================
    const cepFields = document.querySelectorAll('#id_cep, input[name*="cep"]');
    cepFields.forEach(function(field) {
        IMask(field, {
            mask: '00000-000',
            lazy: false,
            placeholderChar: '_'
        });

        field.placeholder = '99999-999';
    });

    // ============================================
    // MÁSCARA: PLACA DE VEÍCULO (AAA-9999 ou AAA9A99)
    // Suporta placas antigas e padrão Mercosul
    // ============================================
    const placaFields = document.querySelectorAll('#id_placa, input[name*="placa"]');
    placaFields.forEach(function(field) {
        IMask(field, {
            mask: [
                {
                    // Placa antiga: AAA-9999
                    mask: 'AAA-0000'
                },
                {
                    // Placa Mercosul: AAA9A99
                    mask: 'AAA0A00'
                }
            ],
            lazy: false,
            placeholderChar: '_',
            prepare: function(value) {
                return value.toUpperCase();
            }
        });

        field.placeholder = 'AAA-9999 ou AAA9A99';
        field.style.textTransform = 'uppercase';
    });

    // ============================================
    // MÁSCARA: ANO (9999)
    // ============================================
    const anoFields = document.querySelectorAll('#id_ano, input[name*="ano"]');
    anoFields.forEach(function(field) {
        IMask(field, {
            mask: '0000',
            lazy: false,
            placeholderChar: '_'
        });

        field.placeholder = 'AAAA';
    });

    // ============================================
    // FUNÇÃO AUXILIAR: Obter valor não formatado
    // ============================================
    window.getUnmaskedValue = function(field) {
        const maskInstance = field.imask;
        if (maskInstance) {
            return maskInstance.unmaskedValue;
        }
        return field.value;
    };

    // ============================================
    // FUNÇÃO AUXILIAR: Obter valor numérico de moeda
    // ============================================
    window.getCurrencyValue = function(field) {
        if (field.classList.contains('masked-currency')) {
            const maskInstance = field.imask;
            if (maskInstance) {
                // Remove 'R$ ' e converte vírgula em ponto
                const value = maskInstance.value.replace('R$ ', '').replace(/\./g, '').replace(',', '.');
                return parseFloat(value) || 0;
            }
        }
        return parseFloat(field.value) || 0;
    };

    // ============================================
    // LOG DE INICIALIZAÇÃO
    // ============================================
    console.log('[IMask] Máscaras inicializadas:');
    console.log('  - CNPJ:', cnpjFields.length, 'campo(s)');
    console.log('  - Telefone:', telefoneFields.length, 'campo(s)');
    console.log('  - Moeda:', moedaFields.length, 'campo(s)');
    console.log('  - CPF:', cpfFields.length, 'campo(s)');
    console.log('  - CEP:', cepFields.length, 'campo(s)');
    console.log('  - Placa:', placaFields.length, 'campo(s)');
    console.log('  - Ano:', anoFields.length, 'campo(s)');
});
