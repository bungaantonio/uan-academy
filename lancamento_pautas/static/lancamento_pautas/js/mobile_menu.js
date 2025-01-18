$(document).ready(function(){
    // Quando o botão de fechar é clicado, esconda o menu lateral
    $("#closeMobileSidebar").click(function () {
        $("#mobileSidebar").addClass("-translate-x-full transition ease-in-out duration-300 transform")
        $("#mobileMenuBackdrop").addClass("opacity-0 transition-opacity ease-linear duration-300")
        $("#mobileMenuBackdrop").removeClass("fixed inset-0");
        $("#mobileSidebar").removeClass("translate-x-0");

        // Leaving: "transition-opacity ease-linear duration-300"
    });

    // Quando o usuário clica no backdrop, esconda o menu lateral
    $("#mobileMenuBackdrop").click(function () {
        $("#mobileSidebar").addClass("-translate-x-full transition-opacity ease-linear duration-300")
        $("#mobileMenuBackdrop").addClass("opacity-0")
        // Leaving: "transition-opacity ease-linear duration-300"
    });

    // Quando o usuário clica no botão para abrir o menu
    $("#openMobileSidebar").click(function () {
        $("#mobileSidebar").removeClass("-translate-x-full");
        $("#mobileMenuBackdrop").removeClass("opacity-0");
        $("#mobileSidebar").addClass("translate-x-0 transition ease-in-out duration-300 transform");
        $("#mobileMenuBackdrop").addClass("fixed inset-0 opacity-100 ");
        // Entering: "transition-opacity ease-linear duration-300"
    });
});