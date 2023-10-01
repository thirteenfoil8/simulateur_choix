$(function(){
    var map, newMarker, markerLocation;
    var MARKERS_MAX = 2;
    var markersGroup = L.layerGroup();
    // Fonction pour initialiser la carte
    function initMap() {
        if (!map) {
            map = L.map('map').setView([46.776, 7.4748], 8);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);
            map.addLayer(markersGroup);
            map.on('click', addMarker);
        } else {
            map.invalidateSize();
        }
    }
    function addMarker(e){
        var markersCount = markersGroup.getLayers().length;
        if (markersCount < MARKERS_MAX) {
            var markerText;
            if (markersCount === 0) {
                document.getElementById('domicile_lat').value = e.latlng.lat;
                document.getElementById('domicile_lng').value = e.latlng.lng;
                markerText = "Domicile";
            } else {
                document.getElementById('travail_lat').value = e.latlng.lat;
                document.getElementById('travail_lng').value = e.latlng.lng;
                markerText = "Travail";
            }
            var marker = L.marker(e.latlng, title=markerText).addTo(markersGroup);
            return;
        }
        markersGroup.clearLayers();
    }
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
        onStepChanged: function (event, currentIndex, priorIndex) {
            // Si l'étape actuelle est celle de la carte (index 1 dans votre cas)
            if (currentIndex === 1) {
                initMap();
            }
        },
        onFinished: function (event, currentIndex) {
            // Soumettre le formulaire lorsque l'utilisateur clique sur "Confirmer"
            $("#form-register").submit();
        }
    });
});