// =============================
// 🔹 CONFIGURACIÓN INICIAL
// =============================
const config = {
    default_distance: "km",
    init_zoom: 11,
    zoomhere_zoom: 15,
    region: "us",
    default_location: "New York, US",
};

let map, geocoder, marker;

$(document).ready(function () {
    const mapCanvas = document.getElementById("map_canvas");
    const address = mapCanvas.dataset.address;
    const iconUrl = mapCanvas.dataset.icon;
    const storeName = mapCanvas.dataset.store;
    const storeAddress = mapCanvas.dataset.storeAddress;
    const detailFlag = document.getElementById("detail")?.value; // bandera

    if ($("#map_canvas").length) {
        geocoder = new google.maps.Geocoder();
        geocoder.geocode({ address, region: config.region }, function (results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                let lat = results[0].geometry.location.lat();
                let lng = results[0].geometry.location.lng();
                let gmap_marker = false;

                if ($("#id_latitude").length) {
                    let val = parseFloat($("#id_latitude").val());
                    if (!isNaN(val)) {
                        lat = val;
                        gmap_marker = true;
                    }
                }

                if ($("#id_longitude").length) {
                    let val = parseFloat($("#id_longitude").val());
                    if (!isNaN(val)) {
                        lng = val;
                    }
                }

                const latlng = new google.maps.LatLng(lat, lng);
                map = new google.maps.Map(document.getElementById("map_canvas"), {
                    zoom: 9,
                    center: latlng,
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                });

                // Crear marcador
                marker = new google.maps.Marker({
                    position: latlng,
                    map: map,
                    draggable: true,
                    icon: iconUrl,
                });
                
                if (detailFlag && detailFlag.trim() !== "") {
                    const infowindow = new google.maps.InfoWindow({
                        content: `<div style="font-size:14px;">
                                    <strong>${storeName}</strong><br>
                                    ${storeAddress}
                                  </div>`,
                    });
                    infowindow.open(map, marker);
                    map.setZoom(13); // 🔎 aumentamos el zoom
                }
                // Actualizar inputs al arrastrar
                google.maps.event.addListener(marker, "drag", function (event) {
                    $("input[name=longitude]").val(event.latLng.lng());
                    $("input[name=latitude]").val(event.latLng.lat());
                });
                google.maps.event.addListener(marker, "dragend", function (event) {
                    $("input[name=longitude]").val(event.latLng.lng());
                    $("input[name=latitude]").val(event.latLng.lat());
                });
            }
        });
    }

    // Recalcular coordenadas si se cambia la dirección
    if ($("#id_address").length) {
        $("#id_address").blur(function () {
            const address = $(this).val();
            if (address) {
                get_coordinate(address, config.region);
            }
        });
    }
});

// =============================
// 🔹 FUNCIÓN GEOCODER
// =============================
function get_coordinate(address, region) {
    geocoder = new google.maps.Geocoder();
    if (!region) region = "us";

    if (address) {
        $("#ajax_msg").html("<p>Loading location</p>");

        geocoder.geocode({ address, region }, function (results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                $("#ajax_msg").html("");
                $("#id_latitude").val(results[0].geometry.location.lat());
                $("#id_longitude").val(results[0].geometry.location.lng());

                map.setZoom(10);
                map.setCenter(results[0].geometry.location);
                marker.setPosition(results[0].geometry.location);
            } else {
                $("#ajax_msg").html(
                    `<p class="text-danger">Google map geocoder failed: ${status}</p>`
                );
            }
        });
    }
}
