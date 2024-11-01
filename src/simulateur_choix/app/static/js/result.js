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
                    let numTripsToMoon = Number((totalDistance / (distanceToMoon*2)).toFixed(2)); // calcule le nombre d'aller-retours Terre-Lune

                    // Calcule la distance que la navette doit parcourir dans le conteneur pour se rendre à la Lune
                    let tripDistancePx = (containerWidth - (earthWidth / 2) - shuttleWidth ); // Soustraire 250 pour prendre en compte la position initiale

                    

                    // Animer la navette se déplaçant vers la Lune et retour
                    function animateShuttle(coefficient = 1) {
                        let shuttle = d3.select("#shuttle");
                        let distanceToTravel = tripDistancePx * coefficient;
                        return new Promise((resolve) => {
                            // Étape 1: Aller
                            shuttle.transition()
                                .duration(2000* coefficient)
                                .ease(d3.easeLinear)
                                .style("transform", `translateX(${distanceToTravel}px) scaleX(-1)`)
                                .on("end", () => {
                                    // Étape 2: Changement de direction à la Lune
                                    shuttle.transition()
                                        .duration(1500* coefficient)
                                        .style("transform", `translateX(${250}px) scaleX(1)`)
                                        .on("end", () => {
                                            // Étape 3: Retour partiel
                                            shuttle.transition()
                                                .duration(2000* coefficient)
                                                .style("transform", `translateX(${-distanceToTravel}px) scaleX(1)`)
                                                .on("end", () => {
                                                    // Étape 4: Changement de direction près de la Terre
                                                        shuttle.transition()
                                                            .duration(1500* coefficient)
                                                            .style("transform", `translateX(-250px) scaleX(-1)`)
                                                            .on("end", resolve);
                                                });
                                        });
                                });
                        });
                    }
                    
                    async function runAnimation() {
                        // Extraire la partie entière et la partie décimale
                        let fullTrips = Math.floor(numTripsToMoon);
                        let partialTripCoefficient = numTripsToMoon - fullTrips;
                    
                        // Effectuer l'animation complète pour la partie entière
                        for (let i = 0; i < fullTrips; i++) {
                            await animateShuttle(1);
                        }
                    
                        // Effectuer la dernière animation avec la partie décimale comme coefficient
                        if (partialTripCoefficient > 0) {
                            await animateShuttle(partialTripCoefficient/2);
                        }
                    }
                    
                    runAnimation();


                    // Mettez à jour le texte pour afficher combien de tours de la Terre la distance parcourue équivaut
                    d3.select("#circumference-info").text(`Équivaut à ${numTripsToMoon} voyages de la Terre à la Lune!`);
                    

                // ########## Language ##############
                let totalTimeDays = parseFloat(dataContainer.getAttribute('data-total-time')); // Supposons que le temps est en jours


                // Calculez combien de fois la série entière pourrait être visionnée
                const NumberDaysForC1 = 100; 
                let numberOfTimesSeriesWatched = Math.floor(totalTimeDays/ NumberDaysForC1);

                // Affichez les masques Dalí pour chaque fois que la série pourrait être visionnée
                let maskContainer = document.getElementById('language-container');
                maskContainer.innerHTML = ''; // Réinitialisez d'abord le conteneur
                for (let i = 0; i < numberOfTimesSeriesWatched; i++) {
                    let maskDiv = document.createElement('div');
                    maskDiv.classList.add('language_mask');
                    maskContainer.appendChild(maskDiv);
                }

                // Mettez à jour le texte pour indiquer combien de fois la série entière pourrait être visionnée
                d3.select("#series-info").text(`Équivaut à apprendre ${numberOfTimesSeriesWatched} langues au niveau C1!`);

                // ########## Price ##############
                let totalPrice = parseFloat(dataContainer.getAttribute('data-total-cost'));
                const priceOfAsupercar = 200000; // prix d'une maison en suisse
                let numberOfsupercars = Math.floor(totalPrice/ priceOfAsupercar);
                // pie chart that we can play with ( destroy it for example)
                let pieChart = echarts.init(document.getElementById('price-container'));
                // specify chart configuration item and data
                let option = {
                    tooltip: {
                        trigger: 'item',
                        formatter: '{a} <br/>{b}: {c} CHF ({d}%)'
                    },
                    legend: {
                        orient: 'vertical',
                        left: 10,
                        data: ['Maison', 'Reste']
                    },
                    series: [
                        {
                            name: 'Prix',
                            type: 'pie',
                            radius: ['50%', '70%'],
                            avoidLabelOverlap: false,
                            label: {
                                show: false,
                                position: 'center'
                            },
                            emphasis: {
                                label: {
                                    show: true,
                                    fontSize: '14',
                                    fontWeight: 'bold'
                                }
                            },
                            labelLine: {
                                show: false
                            },
                            data: [
                                {value: numberOfsupercars, name: 'Maison'},
                                {value: 1, name: 'Reste'}
                            ]
                        }
                    ]
                };
                // use configuration item and data specified to show chart
                pieChart.setOption(option);
                // Mettez à jour le texte pour indiquer combien de fois la série entière pourrait être visionnée
                d3.select("#price-info").text(`Équivaut à ${numberOfsupercars} Porsche 911 Turbo S!`);
                
                // ########## CO2 ##############
                let totalCO2 = parseFloat(dataContainer.getAttribute('data-total-emissions'));
                const CO2perBallon = 4322; // kg de CO2 par vol
                let numberOfBubbles = Math.floor(totalCO2 / CO2perBallon);
                d3.select("#CO2-info").text(`Équivaut à ${numberOfBubbles} mongolfières rempli de CO2!`);
                console.log("Total CO2:", totalCO2);
                console.log("Number of Bubbles:", numberOfBubbles);
                // Dimensions and SVG setup
                const width_bubble = 1000;
                const height_bubble = 500;
                var svg_bubble = d3.select("#bubble")
                    .append("svg")
                    .attr("width", width_bubble)
                    .attr("height", height_bubble);
                function update_bubble(num_bubbles) {
                    
                    const radius = 50;

                    // Clear any existing SVG and create a new one
                    svg_bubble.selectAll("*").remove();

                    const data = d3.range(num_bubbles).map(() => ({
                        x: Math.random() * width_bubble,
                        y: Math.random() * height_bubble
                    }));
                    

                    // Initialize circles with fixed properties
                    var node = svg_bubble.append("g")
                        .selectAll("circle")
                        .data(data)  // Creates an array [0, 1, 2, ..., num_bubbles-1]
                        .enter()
                        .append('circle')
                        .attr('cx', width_bubble / 2)
                        .attr('cy', height_bubble / 2)
                        .attr("r", radius)
                        .style('fill', '#69b3a2')  // Static color for all bubbles
                        .style("stroke", "black")
                        .style("opacity", 1)
                        .call(d3.drag()
                            .on("start", dragstarted)
                            .on("drag", dragged)
                            .on("end", dragended)
                        );

                    // Force simulation for non-overlapping bubbles
                    var simulation = d3.forceSimulation()
                    .force("center", d3.forceCenter().x(0).y(0)) // Attraction to the center of the svg area
                    .force("charge", d3.forceManyBody().strength(300)) // Nodes are attracted one each other of value is > 0
                    .force("collide", d3.forceCollide().strength(0.9).radius(radius).iterations(1)) // Force that avoids circle overlapping

                    simulation
                        .nodes(data)
                        .on("tick", function(d){
                        node
                        .attr("transform", (d) => "translate(" + d.x + "," + d.y + ")")
                        });

                    // Dragging functions
                    function dragstarted(event, d) {
                        if (!event.active) simulation.alphaTarget(0.03).restart();
                        d.fx = d.x;
                        d.fy = d.y;
                    }

                    function dragged(event, d) {
                        d.fx = event.x;
                        d.fy = event.y;
                    }

                    function dragended(event, d) {
                        if (!event.active) simulation.alphaTarget(0.03);    
                        d.fx = null;
                        d.fy = null;
                    }
                }

                // Call the function with the calculated number of bubbles
                update_bubble(numberOfBubbles);

                }
            },
            onFinished: function (event, currentIndex) {
            }
        });
    });
});
