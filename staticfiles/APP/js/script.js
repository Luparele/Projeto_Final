document.addEventListener('DOMContentLoaded', function() {
    // Adiciona classes de estilo para inputs e textareas dentro de formulários
    const allFormInputs = document.querySelectorAll('.auth-form input, .auth-form textarea, .contact-form input, .contact-form textarea, .product-form input, .product-form textarea');

    allFormInputs.forEach(input => {
        if (input.type !== 'submit') {
            input.classList.add('form-input-style');
        }
    });

    // Garante que o botão de submit dentro dos formulários tenha a classe btn-primary
    const allFormButtons = document.querySelectorAll('.auth-form button[type="submit"], .contact-form button[type="submit"], .product-form button[type="submit"]');
    allFormButtons.forEach(button => {
        button.classList.add('btn-primary');
    });

    // Lógica para o vídeo de fundo no hero (se tiver)
    const heroVideo = document.getElementById('heroVideo');
    if (heroVideo) {
        heroVideo.play().catch(error => {
            console.log("Autoplay blocked:", error);
            // Fallback para imagem ou mensagem ao usuário se o autoplay for bloqueado
        });
    }

    // NOVA LÓGICA: Carrossel de Parceiros
    const carouselContent = document.querySelector('.carousel-content');
    if (carouselContent) {
        const carouselItems = Array.from(carouselContent.children); // Converte NodeList para Array
        if (carouselItems.length > 0) {
            // Duplica os itens para criar um efeito de rolagem contínua
            carouselItems.forEach(item => {
                const clone = item.cloneNode(true);
                carouselContent.appendChild(clone);
            });

            // Inicia a animação
            let scrollAmount = 0;
            const scrollSpeed = 0.5; // Ajuste a velocidade da rolagem (pixels por frame)

            function scrollCarousel() {
                scrollAmount += scrollSpeed;
                // Reseta a posição quando metade do conteúdo duplicado é rolado
                // Isso evita que o carrossel role indefinidamente para a direita
                if (scrollAmount >= carouselContent.scrollWidth / 2) {
                    scrollAmount = 0; // Volta ao início para o efeito contínuo
                }
                carouselContent.style.transform = `translateX(-${scrollAmount}px)`;
                requestAnimationFrame(scrollCarousel);
            }
            requestAnimationFrame(scrollCarousel);
        } else {
            console.log("Carrossel de parceiros encontrado, mas sem itens.");
        }
    } else {
        console.log("Elemento .carousel-content não encontrado.");
    }
});