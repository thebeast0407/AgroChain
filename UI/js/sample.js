var map;
     var infowindow;

     function initMap() {
       var pyrmont = {lat: -31.867, lng: 151.195};

       map = new google.maps.Map(document.getElementById('map'), {
         center: pyrmont,
         zoom: 15
       });

       infowindow = new google.maps.InfoWindow();
       var service = new google.maps.places.PlacesService(map);
       service.nearbySearch({
         location: pyrmont,
         radius: 500,
         type: ['store']
       }, callback);
     }

     function callback(results, status) {
       if (status === google.maps.places.PlacesServiceStatus.OK) {
         for (var i = 0; i < results.length; i++) {
           createMarker(results[i]);
         }
       }
     }

     function createMarker(place) {
       var placeLoc = place.geometry.location;
       var marker = new google.maps.Marker({
         map: map,
         position: place.geometry.location
       });

       google.maps.event.addListener(marker, 'click', function() {
         infowindow.setContent(place.name);
         infowindow.open(map, this);
       });
     }
     //initMap();
     var mapOptions = {
    zoom: 8,
    center: new google.maps.LatLng(-34.397, 150.644)
  };
  var map = new google.maps.Map($("#map")[0], mapOptions);

  // listen for the window resize event & trigger Google Maps to update too
  $(window).resize(function() {
    // (the 'map' here is the result of the created 'var map = ...' above)
    google.maps.event.trigger(map, "resize");
  });
});
