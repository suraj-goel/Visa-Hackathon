$(document).ready(function () {
    //Fixing jQuery Click Events for the iPad
    var ua = navigator.userAgent,
        event = (ua.match(/iPad/i)) ? "touchstart" : "click";
    if ($('.table').length > 0) {
        $('.table .header').on(event, function () {
            $(this).toggleClass("active", "").nextUntil('.header').css('display', function (i, v) {
                return this.style.display === 'table-row' ? 'none' : 'table-row';
            });
        });
    }
})


var data = '{{ data|tojson }}';
var currentLocation = '{{ currentLocation|tojson }}'
var jsonData = JSON.parse(data);
var currentLocationJSONData = JSON.parse(currentLocation)
console.log(currentLocationJSONData)
function initMap() {

    var india = {
        lat: 20.5937,
        lng: 78.9629
    };
    var map;
    if (jsonData.length == 0)
        map = new google.maps.Map(
            document.getElementById('map'), {
            zoom: 4,
            center: india
        });
    else
        map = new google.maps.Map(
            document.getElementById('map'), {
            zoom: 7,
            center: {
                lat: parseFloat(jsonData[0].Latitude),
                lng: parseFloat(jsonData[0].Longitude)
            }
        });


    var infowindow = new google.maps.InfoWindow();

    var marker, i;

    for (i = 0; i < jsonData.length; i++) {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(parseFloat(jsonData[i].Latitude), parseFloat(jsonData[i].Longitude)),
            map: map
        });
        if (parseInt(jsonData[i].distance) === 0) {

            marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png')
        }


        google.maps.event.addListener(marker, 'mouseover', (function (marker, i) {
            return function () {
                infowindow.setContent(jsonData[i].RegisteredName);
                infowindow.open(map, marker);
            }
        })(marker, i));

        google.maps.event.addListener(marker, 'mouseout', (function (marker, i) {
            return function () {
                infowindow.close();
            }
        })(marker, i));


        google.maps.event.addListener(marker, 'click', (function (marker, i) {
            return function () {
                if (parseInt(jsonData[i].distance) !== 0)
                    window.location.href = '/merchant/' + jsonData[i].MerchantID;
            }
        })(marker, i));
    }
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(parseFloat(currentLocationJSONData.Latitude), parseFloat(currentLocationJSONData.Longitude)),
        map: map
    });
    marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png')
}


(() => {
    let customSelects = document.querySelectorAll(".custom-dropdown__select");
    customSelects.forEach(el => {
        if (el.disabled)
            el.parentNode.classList.add("custom-dropdown--disabled");
    })
})()