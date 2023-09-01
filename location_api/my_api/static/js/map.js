$(document).ready(function() {
    var map;
    var geocoder;

    // Initialize the map
    function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: 0, lng: 0},
            zoom: 8
        });

        geocoder = new google.maps.Geocoder();

        var input = document.getElementById('locationInput');
        var searchBox = new google.maps.places.SearchBox(input);

        searchBox.addListener('places_changed', function() {
            var places = searchBox.getPlaces();

            if (places.length === 0) {
                return;
            }

            var place = places[0];
            if (!place.geometry) {
                console.log("Place details not found");
                return;
            }

            // Display the location on the map
            displayLocationOnMap(place.geometry.location);
        });
    }

    function displayLocationOnMap(location) {
        map.setCenter(location);

        var marker = new google.maps.Marker({
            map: map,
            position: location
        });
    }

    initMap();
});




