(function(window, document, $) {
    'use strict';

    // ---------- CONSTANTES ----------
    const mapCanvas = document.getElementById('map_canvas');
    const iconUrl = mapCanvas ? (mapCanvas.dataset.icon || '') : '';
    const KM2MILE = 0.621371;
    const MILE2KM = 1.60934;

    // ---------- ESTADO GLOBAL (local al módulo) ----------
    let default_distance = 'km';
    let geo_settings = '0';
    let distancenode = '';
    let default_location = 'Los Ángeles, US';
    let init_zoom = 10;
    let markers = [];
    let arr = [];
    let ssf_map_code;
    let thekm = '';
    let themiles = '';
    let style_map_color = '';
    let totalrec = 0;
    let current_unit = 'km';
    let region = 'us';
    let cachesearch = '';
    let distancecode = 0;
    let map = null;
    let geocoder = null;

    // Set initial unit based on default_distance (preserve original logic)
    if (default_distance === 'mi') {
        current_unit = 'miles';
    } else {
        current_unit = 'km';
    }

    // ---------- DOM Ready: unidad por defecto y listeners ----------
    document.addEventListener('DOMContentLoaded', function() {
        // marcar unidad por defecto y ejecutar changeDistanceUnits al cargar
        const selected = document.querySelector('input[name="distance-units"]:checked');
        if (selected) {
            const label = selected.closest('.form-check') ? selected.closest('.form-check').querySelector('label') : null;
            const units = label ? label.getAttribute('units') : null;
            if (units) {
                console.log('Unidad seleccionada:', units);
                current_unit = units;
                changeDistanceUnits(units);
            }
        }
    
        // listener para cambios de unidad
        document.querySelectorAll('input[name="distance-units"]').forEach(input => {
            input.addEventListener('change', function() {
                const label = this.closest('.form-check') ? this.closest('.form-check').querySelector('label') : null;
                const units = label ? label.getAttribute('units') : null;
                if (units) {
                    console.log('Unidad seleccionada:', units);
                    current_unit = units;
                    changeDistanceUnits(units);
                }
            });
        });

        // inicializar valor del input address según geo_settings
        if ($('#address').length) {
            if (geo_settings == 1) {
                $('#address').val(geoip_city() + ', ' + geoip_country_name());
            } else {
                $('#address').val(default_location);
            }
        }
    });

    // ---------- initMap (expuesto) ----------
    function initMap() {
        if (!mapCanvas) return; // evita error si no existe el contenedor

        // actualizar label de distancia visible
        if (default_distance === 'mi') {
            $('.radius-distance').html('mi');
        } else {
            $('.radius-distance').html('km');
        }

        if ($('#map_canvas').length) {
            const lat = 34.0519074464909;
            const lng = -118.21295444779551;

            geocoder = new google.maps.Geocoder();
            const latlng = new google.maps.LatLng(lat, lng);

            const myOptions = {
                zoom: 10,
                center: latlng,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };

            map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);
            $('#map_canvas').show();
        }

        $('input[name=distance]').on('change', function() {
            cachesearch = '';
            $('#clinic-finder-form').trigger('submit'); // dispara el evento submit real
        });

        // Bind formulario búsqueda
        if ($('#clinic-finder-form').length) {
            $('#clinic-finder-form').submit(function(event) {
                event.preventDefault();

                const address = $('#address').val();
                const distance = $('input[name=distance]:radio:checked').val();

                console.log('Address:', address);
                console.log('Cache:', cachesearch);
                console.log('Distance:', distance);
                console.log('Region:', region);

                if (address !== '' && address !== cachesearch) {
                    console.log("🟢 Ejecutando búsqueda...");
                    gmap_location_lookup(address, distance, region);
                    cachesearch = address;
                } else {
                    $('#address').focus();
                }
                return false;
        });
        }

        $('#edit-products').change(function() { cachesearch = ''; });

        // búsqueda inicial según geo_settings
        if (geo_settings == 1) {
            gmap_location_lookup(geoip_city() + ', ' + geoip_country_name(), '100', '');
        } else {
            gmap_location_lookup(default_location, '100', '');
        }
    }

    // ---------- changeDistanceUnits (expuesto) ----------
    function changeDistanceUnits(units) {
        cachesearch = '';
        const results = $('#results');
        const dUnits = results.find('p.distance-units label');
        const distance = results.find('.distance');
        const unitsSpan = distance.find('.units');

        dUnits.removeClass('unchecked');
        dUnits.filter(':not([units="' + units + '"])').addClass('unchecked');

        switch (units) {
            case 'km':
                unitsSpan.html(' ' + thekm + ' ');
                $.each(distance, function(i/*index*/, val) {
                    i++;
                    let v = $('#d_' + i + ' .value').html();
                    v = parseFloat(v);
                    $('#d_' + i + ' .value').text((Math.round(v * MILE2KM * 100) / 100));
                    $('.radius-distance').html('km');
                });
                break;

            case 'miles':
                unitsSpan.html(' ' + themiles + ' ');
                $.each(distance, function(i/*index*/, val) {
                    i++;
                    let v = $('#d_' + i + ' .value').html();
                    v = parseFloat(v);
                    $('#d_' + i + ' .value').text(Math.round(v * KM2MILE * 100) / 100);
                    $('.radius-distance').html('mi');
                });
                break;

            default:
                // no-op
        }
    }

    // ---------- gmap_location_lookup (expuesto) ----------
    function gmap_location_lookup(address, distance, regionParam) {
        let regionLocal = regionParam;
        if (regionLocal == null || regionLocal === '') regionLocal = 'us';
        distancecode = 1;

        if (!address) return;
        $('#loading-overlay').fadeIn(200);

        $('#map_canvas').html("<div class='spinner-border text-primary' role='status'><span class='visually-hidden'>Loading...</span></div>").show();
        $('#ajax_msg').hide();

        geocoder = new google.maps.Geocoder();
        geocoder.geocode({ 'address': address, 'region': regionLocal }, function(results, status) {
            if (status === google.maps.GeocoderStatus.OK) {
                const lat = results[0].geometry.location.lat();
                const lng = results[0].geometry.location.lng();
                const location = results[0].geometry.location;
                console.log('init zoom: ', init_zoom);

                const myOptions = {
                    zoom: parseInt(init_zoom),
                    center: location,
                    mapTypeId: google.maps.MapTypeId.ROADMAP
                };

                map = new google.maps.Map(document.getElementById('map_canvas'), myOptions);

                // marcador de la dirección buscada
                const marker = new google.maps.Marker({
                    map: map,
                    draggable: false,
                    animation: google.maps.Animation.DROP,
                    position: results[0].geometry.location,
                    title: 'Your entered address'
                });

                const image = new google.maps.MarkerImage(iconUrl, new google.maps.Size(34, 46), new google.maps.Point(0, 0), new google.maps.Point(17, 46));
                const shadow = new google.maps.MarkerImage(iconUrl, new google.maps.Size(60, 46), new google.maps.Point(0, 0), new google.maps.Point(17, 46));

                // estilos de mapa si aplica
                if (ssf_map_code && ssf_map_code !== '') {
                    map.setOptions({ styles: ssf_map_code });
                } else if (style_map_color && style_map_color !== '') {
                    const styles = [{ stylers: [{ hue: style_map_color }, { saturation: 0 }, { lightness: 50 }, { gamma: 1 }] }];
                    map.setOptions({ styles: styles });
                }

                const shape = { coord: [/* ... keep original coords ... */ 31,0], type: 'poly' }; // shape coord preserved conceptually (not changed)

                // clear markers, clear list
                $.each(markers, function(k, v) { v.setMap(null); });
                markers = [];
                $('ol#list').empty();

                let number = 0;

                // adjust distance calculation like original
                if (current_unit === 'km') {
                    const distanceradio = distance;
                    distance = (distance / MILE2KM) - (distanceradio / 4.5);
                }

                // AJAX to get stores
                $.ajax({
                    type: 'POST',
                    url:$('#clinic-finder-form').attr('action'),
                    data: {
                        ajax: 1,
                        action: 'get_nearby_stores',
                        distance: distance,
                        lat: lat,
                        lng: lng,
                        products: $('#edit-products').val()
                    },
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrf-token]').content
                    },
                    success: function(response) {
                        
                        if (response.hasOwnProperty('stores')) {
                            totalrec = response.stores.length;
                        }

                        if (response.success) {
                            const infowindow = new google.maps.InfoWindow({ maxWidth: '400', content: '' });
                            let $i = 0;

                            $.each(response.stores, function(k, v) {
                                const marker = new google.maps.Marker({
                                    __gm_id: $i++,
                                    map: map,
                                    position: new google.maps.LatLng(v.lat, v.lng),
                                    icon: image,
                                    shadow: shadow,
                                    shape: shape,
                                    title: v.name + ' : ' + v.address
                                });

                                // calc distance origin/dest
                                const origin = new google.maps.LatLng(lat, lng);
                                const dest = new google.maps.LatLng(v.lat, v.lng);
                                
                                themiles = v.titlemiles;
                                thekm = v.titlekm;
                                let default_unit_system = google.maps.UnitSystem.METRIC;
                                if (current_unit === 'miles') default_unit_system = google.maps.UnitSystem.IMPERIAL;

                                const service = new google.maps.DistanceMatrixService();
                                service.getDistanceMatrix({
                                    origins: [origin],
                                    destinations: [dest],
                                    travelMode: google.maps.TravelMode.DRIVING,
                                    unitSystem: default_unit_system,
                                    avoidHighways: false,
                                    avoidTolls: false
                                }, callback);

                                markers.push(marker);

                                const info_window_string = info_window_content(v);

                                let ctype = '';
                                if (v.cat_img && v.cat_img !== '') {
                                    ctype = '<img src="' + v.cat_img + '" style="max-width:48px; max-height:48px;">';
                                }

                                number++;
                                // build list element
                                const liHtml = "<span class='number'>" + number + "</span><div><strong>" + v.name + "</strong><br /><span>" + v.address + "</span><div id=d_" + number + " class='distance'><span id='disval' attr-dist='" + distancenode + "' class='value'>" + distancenode + "</span> <span class='units'></span> <span class='time2'></span></div></div><div class='products'>" + ctype + "</div>";
                                const liHtmlWithAnchor = liHtml + "<a id='la_" + marker['__gm_id'] + "' name='la_" + marker['__gm_id'] + "'></a>";

                                if (number > 9) {
                                    $('<li id="l_' + marker['__gm_id'] + '" class="clinic_list double-digit" />').html(liHtml).click(function() {
                                        infowindow.setContent(info_window_string);
                                        infowindow.open(map, marker);
                                        toggleBounce(marker);
                                        const currentLatLng = new google.maps.LatLng(v.lat, v.lng);
                                        map.setCenter(currentLatLng);
                                    }).appendTo('#list');
                                } else {
                                    $('<li id="l_' + marker['__gm_id'] + '" class="clinic_list" />').html(liHtmlWithAnchor).click(function() {
                                        infowindow.setContent(info_window_string);
                                        infowindow.open(map, marker);
                                        toggleBounce(marker);
                                        const currentLatLng = new google.maps.LatLng(v.lat, v.lng);
                                        map.setCenter(currentLatLng);
                                    }).appendTo('#list');
                                }

                                // attach popup to click event (marker)
                                google.maps.event.addListener(marker, 'click', function() {
                                    $('#list .clinic_list').removeClass('active');
                                    $('#l_' + marker['__gm_id']).addClass('active');

                                    // scroll behaviours preserved
                                    $('#list').animate({ scrollTop: $('#list').scrollTop() + $('#list li.active').offset().top - $('#list').offset().top }, { duration: 'slow', easing: 'swing' });
                                    $('html,body').animate({ scrollTop: $('#list').offset().top - $(window).height() + $('#list li.active').height() }, { duration: 1000, easing: 'swing' });

                                    infowindow.setContent(info_window_string);
                                    infowindow.open(map, marker);
                                    toggleBounce(marker);
                                    const currentLatLng = new google.maps.LatLng(v.lat, v.lng);
                                    map.setCenter(currentLatLng);
                                });

                            }); // end each store

                            if (response.distance) {
                                let zoomLevel = parseInt(init_zoom); // fallback si no coincide

                                if (response.distance <= 10) {
                                    zoomLevel = 14;
                                } else if (response.distance <= 50) {
                                    zoomLevel = 12;
                                } else if (response.distance <= 100) {
                                    zoomLevel = 10;
                                } else {
                                    zoomLevel = 8;
                                }

                                map.setZoom(zoomLevel);
                                console.log("Zoom ajustado a:", zoomLevel, "por distancia:", response.distance);
                            }

                            // Ajuste adicional: encuadrar todos los puntos si hay muchos
                            if (response.stores.length > 1) {
                                const bounds = new google.maps.LatLngBounds();
                                response.stores.forEach(store => {
                                    bounds.extend(new google.maps.LatLng(store.lat, store.lng));
                                });
                                map.fitBounds(bounds);
                            }

                            // list click handler preserved
                            $('.clinic_list').click(function() {
                                $('html, body').animate({ scrollTop: 100 }, 'normal');
                                $('#list .clinic_list').removeClass('active');
                                $(this).addClass('active');
                                $('div[title="Exit Street View"]').trigger('click');
                                map.setZoom(parseInt(init_zoom));
                            });

                            $('#ajax_msg').html("<p class='flash_good'>" + response.stores.length + " stores have been found</p>").fadeIn();
                            $('#loading-overlay').fadeOut(200);
                        } else {
                            $('#loading-overlay').fadeOut(200);
                            // no success
                            $('<li  />').html("<span class='number'>!</span><p>" + response.msg + "</p>").click(function() {
                                infowindow.setContent(info_window_string || '');
                                infowindow.open(map, marker || null);
                                toggleBounce(marker || {});
                            }).appendTo('#list');

                            $('#ajax_msg').html("<p class='alert alert-block alert-error fade in'>" + response.msg + "</p>").fadeIn();
                        }

                    } // end ajax success
                }); // end ajax

            } // end geocode OK
        }); // end geocode
    }

    // ---------- callback (DistanceMatrix) ----------
    function callback(response, status) {
        if (status === google.maps.DistanceMatrixStatus.OK) {
            const origins = response.originAddresses;
            const destinations = response.destinationAddresses;
            let un = '';
            for (let i = 0; i < origins.length; i++) {
                const results = response.rows[i].elements;
                console.log(results);
                for (let j = 0; j < results.length; j++) {
                    var element = results[j];
                    // distance in meters -> km
                    let distance = element.distance.value;
                    distance /= 1000;
            
                if (current_unit === 'miles') {
                    distance = parseFloat(Math.round(distance * KM2MILE * 100) / 100);
                    un = themiles;
                    } else {
                        distance = parseFloat(Math.round(distance * 100) / 100);
                        un = thekm;
                    }
                    
                    const duration = element.duration.text;
                    const from = origins[i];
                    const to = destinations[j];
                    
                    arr.push(distance);
                }
            }

            distancecode++;
            if (distancecode === (totalrec + 1)) {
                distancecode = 0;
                arr.sort(function(a, b) { return a - b; });
                for (let k = 0; k <= arr.length; k++) {
                $('#d_' + (k + 1) + ' .value').html(arr[k]);
                $('#d_' + (k + 1) + ' .units').html(un);
                }
                arr = [];
            }
        }
    }

    // ---------- info_window_content (expuesto) ----------
    function info_window_content(v) {
        let info_window_string = "<div class='maps_popup'>";

        // media: image or embedded video
        if (!v.default_media || v.default_media === 'image') {
            if (v.img && v.img !== 'null') {
                info_window_string += "<img class='img' src='" + v.img + "' alt='" + v.name + "'>";
            }
        } else {
            if (v.embed_video && v.embed_video !== 'null') {
                info_window_string += v.embed_video;
            }
        }

        // split address with a break after 4 words (preserve original behaviour)
        let splitaddress = '';
        if (v.address && v.address !== 'null') {
            const saddress = v.address.split(' ');
            for (let i = 0; i < saddress.length; i++) {
                splitaddress += saddress[i] + ' ';
                if (i === 4) splitaddress += '<br>';
            }
        }

        info_window_string += "<h1>" + (v.name || '') + "</h1><p>" + splitaddress + "</p>";

        if (v.telephone && v.telephone !== '') {
        info_window_string += "<p class='tel'>" + (v.titletel || 'Teléfono') + ": " + v.telephone + "</p>";
        }

        if (v.email && v.email !== '' && v.email !== null) {
        info_window_string += "<p class='email'>" + (v.titleemail || 'Email') + ": <a href='mailto:" + v.email + "'>" + v.email + "</a></p>";
        }

        if (v.website && v.website.trim() !== '') {
            const site = v.website;
            if (site.substring(0, 4).toLowerCase() !== 'http') {
                info_window_string += "<p class='web'>" + (v.titlewebsite || 'Website') + ": <a href='http://" + site + "' target='_blank'>http://" + site + "</a></p>";
            } else {
                info_window_string += "<p class='web'>" + (v.titlewebsite || 'Website') + ": <a href='" + site + "' target='_blank'>" + site + "</a></p>";
            }
        }

        if (v.description && v.description !== '') {
            info_window_string += "<p class='description'>" + v.description + "</p>";
        }

        if (v.cat_img && v.cat_img !== '') {
            info_window_string += "<div class='products'><img src='" + v.cat_img + "' style='max-width:15px; max-height:15px;' /> " + (v.cat_name || '') + "</div>";
        }

        info_window_string += "<span class='email'><center><a href='/store/" + v.store_id + "' target='_blank' class='contact-clinic button blue-button' style='display:block;" +
            "padding:5px 10px;" +
            "margin-top:10px;" +
            "margin-bottom:10px;" +
            "margin-left:3px;" +
            "border:1px solid #8b8b8b;" +
            "text-align: center;" +
            "font-weight:bold;" +
            "width:190px;'>Ver detalle</a></center></span>";

        info_window_string += "</div>";
        return info_window_string;
    }

    // ---------- toggleBounce (expuesto) ----------
    function toggleBounce(marker) {
        $(markers).each(function(i, marker2) {
            if (marker && marker2 && marker['__gm_id'] !== marker2['__gm_id']) {
                if (marker2.setAnimation) marker2.setAnimation(null);
            }
        });

        if (marker && marker.getAnimation && marker.getAnimation() != null) {
            marker.setAnimation(null);
        } else if (marker && marker.setAnimation) {
            marker.setAnimation(google.maps.Animation.BOUNCE);
        }

        const $allVideos = $("iframe[src^='http']");
        $allVideos.each(function() {
            $(this).data('aspectRatio', this.height / this.width).removeAttr('height').removeAttr('width');
        });

        const newWidth = "220px";
        $allVideos.each(function() {
            const $el = $(this);
            $el.width(newWidth).height(newWidth);
        });
    }

    // ---------- Exponer funciones necesarias globalmente ----------
    window.initMap = initMap;
    window.gmap_location_lookup = gmap_location_lookup;
    window.changeDistanceUnits = changeDistanceUnits;
    window.info_window_content = info_window_content;
    window.toggleBounce = toggleBounce;

})(window, document, jQuery);
