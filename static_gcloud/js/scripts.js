/*!
* Start Bootstrap - Grayscale v7.0.6 (https://startbootstrap.com/theme/grayscale)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // Máscara CNPJ
    function applyCnpjMask(value) {
        // Remove tudo que não é dígito
        value = value.replace(/\D/g, '');
        
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

    // Aplicar máscara CNPJ ao campo
    const cnpjField = document.getElementById('id_cnpj');
    if (cnpjField) {
        cnpjField.addEventListener('input', function(e) {
            const cursorPosition = e.target.selectionStart;
            const oldValue = e.target.value;
            const newValue = applyCnpjMask(e.target.value);
            
            // Atualiza o valor
            e.target.value = newValue;
            
            // Calcula a nova posição do cursor
            const diff = newValue.length - oldValue.length;
            const newCursorPosition = cursorPosition + diff;
            
            // Reposiciona o cursor
            e.target.setSelectionRange(newCursorPosition, newCursorPosition);
        });

        // Também aplicar máscara ao colar
        cnpjField.addEventListener('paste', function(e) {
            setTimeout(() => {
                e.target.value = applyCnpjMask(e.target.value);
            }, 10);
        });
    }

});