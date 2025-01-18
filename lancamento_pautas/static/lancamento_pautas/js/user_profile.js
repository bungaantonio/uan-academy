$(document).ready(function() {
    // Abrir o menu lateral
    $('#open-sidebar').on('click', function() {
        $('.off-canvas-menu').removeClass('hidden');
        $('.off-canvas-menu').addClass('translate-x-0');
    });

    // Fechar o menu lateral
    $('.close-sidebar').on('click', function() {
        $('.off-canvas-menu').addClass('-translate-x-full');
        $('.off-canvas-menu').removeClass('translate-x-0');
    });

    // Fechar o menu lateral ao clicar fora
    $('.off-canvas-menu-backdrop').on('click', function() {
        $('.off-canvas-menu').addClass('-translate-x-full');
        $('.off-canvas-menu').removeClass('translate-x-0');
    });
});