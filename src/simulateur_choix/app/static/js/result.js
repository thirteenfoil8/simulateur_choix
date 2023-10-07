// Supposons que la circonférence de la Terre est d'environ 40,075 km
document.addEventListener("DOMContentLoaded", function() {
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
                finish : 'Résultat',
                current : ''
            },
            onStepChanged: function (event, currentIndex, priorIndex) {
                // Si l'étape actuelle est celle de la carte (index 1 dans votre cas)
                if (currentIndex === 1) {
                    let dataContainer = document.getElementById('dataContainer');
                    let totalDistance = parseFloat(dataContainer.getAttribute('data-total-distance'));

                    const earthCircumference = 40075;
                    let numEarthRounds = Math.floor(totalDistance / earthCircumference); // calcule le nombre de tours de la Terre

                    // Animer la rotation de la Terre avec D3.js
                    d3.select("#earth")
                        .transition()
                        .duration(2000 * numEarthRounds) // chaque tour prend 2 secondes
                        .ease(d3.easeLinear)
                        .styleTween("transform", function() {
                            return d3.interpolateString("rotate(0deg)", `rotate(${360 * numEarthRounds}deg)`);
                        });

                    // Mettez à jour le texte pour afficher combien de tours de la Terre la distance parcourue équivaut
                    d3.select("#circumference-info").text(`Équivaut à ${numEarthRounds} tours de la Terre!`);
                    

                    // ##########    DALI ##############
                let totalTimeDays = parseFloat(dataContainer.getAttribute('data-total-time')); // Supposons que le temps est en jours

                // Supposons que chaque épisode de "La Casa de Papel" dure en moyenne 50 minutes.
                // Convertissez le temps total en minutes pour une comparaison.
                let totalTimeMinutes = totalTimeDays * 24 * 60;

                // Calculez combien de fois la série entière pourrait être visionnée
                const casaDePapelSeriesDurationMinutes = 2660; 
                let numberOfTimesSeriesWatched = Math.floor(totalTimeMinutes / casaDePapelSeriesDurationMinutes);

                // Affichez les masques Dalí pour chaque fois que la série pourrait être visionnée
                let maskContainer = document.getElementById('dali-mask-container');
                maskContainer.innerHTML = ''; // Réinitialisez d'abord le conteneur
                for (let i = 0; i < numberOfTimesSeriesWatched; i++) {
                    let maskDiv = document.createElement('div');
                    maskDiv.classList.add('dali-mask');
                    maskContainer.appendChild(maskDiv);
                }

                // Mettez à jour le texte pour indiquer combien de fois la série entière pourrait être visionnée
                d3.select("#series-info").text(`Équivaut à regarder "La Casa de Papel" ${numberOfTimesSeriesWatched} fois!`);
                }
            },
            onFinished: function (event, currentIndex) {
            }
        });
    });
});
