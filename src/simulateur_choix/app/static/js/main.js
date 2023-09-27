$(function(){
    $("#form-total").steps({
        headerTag: "h2",
        bodyTag: "section",
        transitionEffect: "fade",
        enableAllSteps: true,
        autoFocus: true,
        transitionEffectSpeed: 500,
        titleTemplate : '<div class="title">#title#</div>',
        labels: {
            previous : 'Précedent',
            next : 'Suivant',
            finish : 'Confirmer',
            current : ''
        },
        onFinished: function (event, currentIndex) {
            // Soumettre le formulaire lorsque l'utilisateur clique sur "Confirmer"
            $("#form-register").submit();
        }
    });
});