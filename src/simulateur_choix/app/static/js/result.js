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
                    let earthWidth = 200;
                    let shuttleWidth = 40;
                    let containerWidth = document.getElementById('space-scene-id').offsetWidth;

                    const distanceToMoon = 384400; // distance moyenne de la Terre à la Lune en km
                    let numTripsToMoon = Math.floor(totalDistance / distanceToMoon); // calcule le nombre d'aller-retours Terre-Lune

                    // Calcule la distance que la navette doit parcourir dans le conteneur pour se rendre à la Lune
                    let tripDistancePx = (containerWidth - (earthWidth / 2) - shuttleWidth ); // Soustraire 250 pour prendre en compte la position initiale

                    

                    // Animer la navette se déplaçant vers la Lune et retour
                    function animateShuttle() {
                        let shuttle = d3.select("#shuttle");
                    
                        return new Promise((resolve) => {
                            // Étape 1: Aller
                            shuttle.transition()
                                .duration(2000)
                                .ease(d3.easeLinear)
                                .style("transform", `translateX(${tripDistancePx}px) scaleX(-1)`)
                                .on("end", () => {
                                    // Étape 2: Changement de direction à la Lune
                                    shuttle.transition()
                                        .duration(1500)
                                        .style("transform", `translateX(${250}px) scaleX(1)`)
                                        .on("end", () => {
                                            // Étape 3: Retour partiel
                                            shuttle.transition()
                                                .duration(2000)
                                                .style("transform", `translateX(${-tripDistancePx}px) scaleX(1)`)
                                                .on("end", () => {
                                                    // Étape 4: Changement de direction près de la Terre
                                                        shuttle.transition()
                                                            .duration(1500)
                                                            .style("transform", `translateX(-250px) scaleX(-1)`)
                                                            .on("end", resolve);
                                                });
                                        });
                                });
                        });
                    }
                    
                    async function runAnimation() {
                        for (let i = 0; i < numTripsToMoon; i++) {
                            await animateShuttle();
                        }
                    }
                    
                    runAnimation();


                    // Mettez à jour le texte pour afficher combien de tours de la Terre la distance parcourue équivaut
                    d3.select("#circumference-info").text(`Équivaut à ${numTripsToMoon} voyages de la Terre à la Lune!`);
                    

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
