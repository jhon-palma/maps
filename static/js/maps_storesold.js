const mapCanvas = document.getElementById("map_canvas");
const iconUrl = mapCanvas.dataset.icon;
var default_distance = "km";
var geo_settings = '0';
var distancenode = '';
var default_location = "Los Ángeles, US";
var init_zoom = 13;
var markers = new Array();
var arr = new Array();
var ssf_map_code;
var thekm = '';
var style_map_color = '';
var totalrec = 0;
var current_unit = 'km';
var region =  "us";
if(default_distance=='mi'){
    current_unit = 'miles';
} else {
    current_unit = 'km';
}

var km2mile = 0.621371;
var mile2km = 1.60934;

cachesearch = '';

document.addEventListener("DOMContentLoaded", function() {
    // Mostrar el valor seleccionado al cargar la página
    const selected = document.querySelector('input[name="distance-units"]:checked');
    if (selected) {
        const label = selected.closest('.form-check').querySelector('label');
        const units = label ? label.getAttribute('units') : null;
        console.log("Unidad seleccionada:", units);
        current_unit = units;
        changeDistanceUnits(units);
    }

    // Mostrar alert cuando cambie la selección
    document.querySelectorAll('input[name="distance-units"]').forEach(input => {
        input.addEventListener('change', function() {
            const label = this.closest('.form-check').querySelector('label');
            const units = label ? label.getAttribute('units') : null;

            console.log("Unidad seleccionada:", units);
            current_unit = units;
            changeDistanceUnits(units);
        });
    });
    if(geo_settings==1){
        $('#address').val(geoip_city()+", "+geoip_country_name());
    } else {
            $('#address').val(default_location);
    }
});

function initMap() {
    if (!mapCanvas) return;

    if(default_distance=='mi'){
		$('.radius-distance').html('mi');
	} else {
		$('.radius-distance').html('km');
	}

    if($('#map_canvas').length) {
        
		var lat = 34.0519074464909;
		var lng = -118.21295444779551;

		// instantiate geocoder
		geocoder = new google.maps.Geocoder();
		// create new latitude / longitude object
		var latlng = new google.maps.LatLng(lat,lng);

		var myOptions = {
			zoom: 10,
			center: latlng,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
		};
		
		map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
		$('#map_canvas').show();
	}

    // var autocomplete = new google.maps.places.Autocomplete($("#address")[0], {});
    // var origin_autocomplete = new google.maps.places.Autocomplete($("#origin-direction")[0], {});

    if($('#clinic-finder-form').length) {

		$('#clinic-finder-form').submit(function(){

			var address = $('#address').val();
////////////////////////////////////
			var distance = $('input[name=distance]:radio:checked').val();    // default 100 radius in km
///////////////////////////////////
			// search for available locations
			if(address != '' && address!=cachesearch) {
				gmap_location_lookup(address, distance, region);
				cachesearch = address;
			} else {
				$('#address').focus();
			}
			
		return false;
		});
	}
	
	$('#edit-products').change(function() {
		cachesearch = '';
	});

    if(geo_settings==1){
		gmap_location_lookup(geoip_city()+', '+geoip_country_name(),'100',''); 	
	} else {
		gmap_location_lookup(default_location,'100',''); 	
	}
}

function changeDistanceUnits(units){
	cachesearch = '';
    var results = $('#results');
    var dUnits = results.find('p.distance-units label');
    var distance = results.find('.distance');
    var unitsSpan = distance.find('.units');
    var valueSpan = distance.find('.value');

//     alert(dUnits + distance + unitsSpan + valueSpan);

    dUnits.removeClass('unchecked');

    dUnits.filter(':not([units="'+units+'"])').addClass('unchecked');
    
    switch (units){
	
      case 'km':
        
		unitsSpan.html(' '+thekm+' ');

        $.each(distance, function(i, val){
          // values are already in kms so just round to 2 decimal places.
	    i++;
	    val = $('#d_'+i+' .value').html();
            val = parseFloat(val);
///////////		
//          $('#d_'+i+' .value').text((Math.round(val / milesToKm * 100) / 100));
          $('#d_'+i+' .value').text((Math.round(val * mile2km * 100) / 100));
		  $('.radius-distance').html('km');
//////////
		
        });
		
      break;  
      
      case 'miles':
	
        unitsSpan.html(' '+themiles+' ');

        $.each(distance, function(i, val){
          // Values are in kms so convert to miles then round down to two decimal places.
          i++;
	    val = $('#d_'+i+' .value').html();
	    val = parseFloat(val);
////////////////////////////////
//          $('#d_'+i+' .value').text(Math.round((val * milesToKm) * 100) / 100);
            $('#d_'+i+' .value').text(Math.round(val * km2mile * 100)/100);
			 $('.radius-distance').html('mi');
///////////////////////////////
        });
	   
      break;

      default:
     }
  }

  function gmap_location_lookup(address,distance,region) {

	if(region==null || region == '') {
		region = 'us';
	}
	
	distancecode = 1;
	
	if(address != '') {
		
		$('#map_canvas').html("<div class='spinner-border text-primary' role='status'><span class='visually-hidden'>Loading...</span></div>").show();
		$('#ajax_msg').hide();
	
		geocoder = new google.maps.Geocoder();
		geocoder.geocode( {'address':address,'region':region}, function(results, status) {
		
			if(status == google.maps.GeocoderStatus.OK) {
			
				var lat = results[0].geometry.location.lat();
				var lng = results[0].geometry.location.lng();
				var location = results[0].geometry.location;
                console.log("init zoom: ", init_zoom);
				
				var myOptions = {
					zoom: parseInt(init_zoom),
					center: location,
					mapTypeId: google.maps.MapTypeId.ROADMAP
				};
				
				map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

				
				var marker = new google.maps.Marker({
					map: map,
					draggable:false,
					animation: google.maps.Animation.DROP,
					position: results[0].geometry.location,
					title:'Your entered address'
				});
				
				 var image = new google.maps.MarkerImage(
					iconUrl,
					new google.maps.Size(34,46),
					new google.maps.Point(0,0),
					new google.maps.Point(17,46)
				 );

				  var shadow = new google.maps.MarkerImage(
					iconUrl,
					new google.maps.Size(60,46),
					new google.maps.Point(0,0),
					new google.maps.Point(17,46)
				  );
				  
				  //patch 2.6 custom map code
				if(ssf_map_code!="" && ssf_map_code!=undefined)
				{
				  map.setOptions({styles: ssf_map_code});	

				} else {

				if(style_map_color!=""){
					  var styles = [
					  {
						stylers: [
						  { hue: style_map_color },
						  { saturation: 0 },
						  { lightness: 50 },
						  { gamma: 1 },
						]
					  }
					];

					map.setOptions({styles: styles});
					}
				}

				  var shape = {
					coord: [31,0,32,1,33,2,33,3,33,4,33,5,33,6,33,7,33,8,33,9,33,10,33,11,33,12,33,13,33,14,33,15,33,16,33,17,33,18,33,19,33,20,33,21,33,22,33,23,33,24,33,25,33,26,33,27,33,28,33,29,33,30,33,31,33,32,32,33,31,34,29,35,26,36,25,37,25,38,24,39,23,40,23,41,22,42,22,43,21,44,20,45,16,45,15,44,14,43,14,42,13,41,13,40,12,39,12,38,11,37,10,36,6,35,4,34,3,33,2,32,1,31,1,30,0,29,0,28,0,27,0,26,0,25,0,24,0,23,0,22,0,21,0,20,0,19,0,18,0,17,0,16,0,15,0,14,0,13,0,12,0,11,0,10,0,9,0,8,0,7,0,6,0,5,1,4,1,3,2,2,3,1,4,0,31,0],
					type: 'poly'
				  };
				
				  
				// clear all markers
				jQuery.each(markers,function(k,v){
					v.setMap(null);
				});

				// clear list
				$('ol#list').empty();
				
				var number = 0;

				
				///////////////
				if(current_unit=='km'){
                    
				  distanceradio = distance;
				  distance = (distance/mile2km)-(distanceradio/4.5); 
				}
				//////////////
				
				
				
				$.ajax({
					type: "POST",
					url: '/get_nearby_stores/',
					data: {
                        'ajax': 1,
                        'action': 'get_nearby_stores',
                        'distance': distance,
                        'lat': lat,
                        'lng': lng,
                        'products': $('#edit-products').val()
                    },
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrf-token]').content  // Obtenemos el token CSRF desde el meta tag
                    },
					success:function(response) {
						console.log(response);

						if (response.hasOwnProperty('stores')) {
							totalrec = response.stores.length;
						}
					
						if( response.success ) {
							var infowindow = new google.maps.InfoWindow({
								maxWidth: "400",
								content: ''
							});
								
							$i = 0;
							jQuery.each( response.stores,function(k,v){
								var marker = new google.maps.Marker({
									__gm_id: $i++,
									map: map,
									position: new google.maps.LatLng(v.lat,v.lng),
									icon: image,
									shadow: shadow,
									shape: shape,
									title: v.name+' : '+v.address
								});
								
								// calc distance
								origin = new google.maps.LatLng(lat, lng);
								dest = new google.maps.LatLng(v.lat,v.lng);
							// set km / miles language	
							themiles = v.titlemiles;
							thekm = v.titlekm;
							/////////////////////
							default_unit_system = google.maps.UnitSystem.METRIC;
							if(current_unit=="km"){
							default_unit_system = google.maps.UnitSystem.METRIC;
							} else if(current_unit=="miles"){
							default_unit_system = google.maps.UnitSystem.IMPERIAL;
							}
							
								var service = new google.maps.DistanceMatrixService();
								service.getDistanceMatrix(
								  {
									origins: [origin],
									destinations: [dest],
									travelMode: google.maps.TravelMode.DRIVING,
									unitSystem: default_unit_system,
									avoidHighways: false,
									avoidTolls: false
								  }, callback);
					  
								// add to markers
								markers.push(marker);
								
								

								// build content string
								var info_window_string = info_window_content(v);
								ctype='';
								if(v.cat_img != '') {
									var ctype = '<img src="'+v.cat_img+'" style="max-width:60px; max-height:60px;" />';
								}
								
								number++
								//distancenode = google.maps.geometry.spherical.computeDistanceBetween(origin, dest).toFixed(2);
								if(number>9){
								$("<li id='l_"+marker['__gm_id']+"' class='clinic_list double-digit' />")
									.html("<span class='number'>"+number+"</span><div><strong>"+v.name+"</strong><br /><span>"+v.address+"</span><div id=d_"+number+" class='distance'><span id='disval' attr-dist='"+distancenode+"' class='value'>"+distancenode+"</span> <span class='units'></span> <span class='time2'></span></div></div><div class='products'>"+ctype+"</div>")
									.click(function(){
										//displayPoint(marker, i);
										infowindow.setContent(info_window_string);
										infowindow.open(map,marker);
										toggleBounce(marker);
										var currentLatLng = new google.maps.LatLng(v.lat,v.lng);
										map.setCenter(currentLatLng);
									})
									.appendTo("#list");
								} else {


								$("<li id='l_"+marker['__gm_id']+"' class='clinic_list' />")
									.html("<span class='number'>"+number+"</span><div><strong>"+v.name+"</strong><br /><span>"+v.address+"</span><div id=d_"+number+" class='distance'><span id='disval' attr-dist='"+distancenode+"' class='value'>"+distancenode+"</span> <span class='units'></span> <span class='time2'></span></div></div><div class='products'>"+ctype+"</div><a id='la_"+marker['__gm_id']+"' name='la_"+marker['__gm_id']+"'></a>")
									.click(function(){
										//displayPoint(marker, i);
										infowindow.setContent(info_window_string);
										infowindow.open(map,marker);
										toggleBounce(marker);
										var currentLatLng = new google.maps.LatLng(v.lat,v.lng);
										map.setCenter(currentLatLng);
										
										
									})
									.appendTo("#list");
								}

								// sort distance

								
								// attach popup to click event
								google.maps.event.addListener(marker, 'click', function() {
								    $('#list .clinic_list').removeClass('active');

									$('#l_'+marker['__gm_id']).addClass('active');
									
									$('#list').animate({ scrollTop: $('#list').scrollTop() + $('#list li.active').offset().top - $('#list').offset().top }, { duration: 'slow', easing: 'swing'});
									$('html,body').animate({ scrollTop: $('#list').offset().top - $(window).height() + $('#list li.active').height() }, { duration: 1000, easing: 'swing'});
									
									
									infowindow.setContent(info_window_string);
									infowindow.open(map,marker);
									toggleBounce(marker);
									var currentLatLng = new google.maps.LatLng(v.lat,v.lng);
									map.setCenter(currentLatLng);
									
								});

							} ); // end loop


							$('.clinic_list').click(function(){
							    $('html, body').animate({scrollTop:100}, 'normal');
								$('#list .clinic_list').removeClass('active');
								$(this).addClass('active');
								$('div[title="Exit Street View"]').trigger('click');
								map.setZoom(parseInt(init_zoom));
								
							 }); 
				
							$('#ajax_msg').html("<p class='flash_good'>"+response.stores.length+" stores have been found</p>").fadeIn();
						} else {
						
							
							$("<li  />")
									.html("<span class='number'>!</span><p>"+response.msg+"</p>")
									.click(function(){
										//displayPoint(marker, i);
										infowindow.setContent(info_window_string);
										infowindow.open(map,marker);
										toggleBounce(marker);
									})
									.appendTo("#list");
							$('#ajax_msg').html("<p class='alert alert-block alert-error fade in'>"+response.msg+"</p>").fadeIn();
						}
						


						//sort_distance();
					}
				});
			}
		});
	}

    

}

function callback(response, status) {
    if (status == google.maps.DistanceMatrixStatus.OK) {
        var origins = response.originAddresses;
        var destinations = response.destinationAddresses;
        
        
    for (var i = 0; i < origins.length; i++) {
      var results = response.rows[i].elements;

      for (var j = 0; j < results.length; j++) {
	  
        var element = results[j];

///////////////  distance is in meter ////////////////////////////////
          var distance = element.distance.value;

	  distance /= 1000;  // conv to km

	  var un = '';
	  if(current_unit=='miles') {
	      distance= parseFloat(Math.round(distance * km2mile *100)/100);
	      un = themiles;
	  }	      
	  else {
 	      distance= parseFloat(Math.round(distance*100)/100);   
	      un = thekm;
        //   alert(un);
	  }

        var duration = element.duration.text;
        var from = origins[i];
        var to = destinations[j];

		arr.push(distance);

      }
    }
	distancecode++;
    // alert(un);
	if(distancecode==(totalrec+1)){
		distancecode=0;
		arr.sort(function(a,b){return a-b});
		
		for(k=0;k<=arr.length;k++){
			$('#d_'+(k+1)+' .value').html(arr[k]);
			$('#d_'+(k+1)+' .units').html(un);
		}
		arr = [];
	}
  } 
}

function info_window_content(v) {

	var info_window_string = "<div class='maps_popup'>";

	if (!v.default_media || v.default_media === 'image') {
        if (v.img && v.img !== 'null') {
            info_window_string += "<img class='img' src='" + v.img + "' alt='" + v.name + "' />";
        }
    } else {
        if (v.embed_video && v.embed_video !== 'null') {
            info_window_string += v.embed_video;
        }
    }

	
	 var splitaddress = "";
	 if(v.address && v.address!='null'){
	 saddress = v.address.split(" ");
	 for(i=0;i<saddress.length;i++){
		splitaddress += saddress[i]+" ";
		 if(i==4){
		  splitaddress += "<br>";
		 }
	 }
	 }
	info_window_string += "<h1>"+v.name+"</h1><p>"+splitaddress+"</p>";

	if(v.telephone != '') {
		info_window_string += "<p class='tel'>"+v.titletel+": "+v.telephone+"</p>";
	}
	if(v.email != '' && v.email !== null) {
		info_window_string += "<p class='email'>"+v.titleemail+": <a href='mailto:"+v.email+"'>"+v.email+"</a></p>";
	}
		
	if (v.website && v.website.trim() !== "") {
        if (v.website.substring(0, 4).toLowerCase() !== "http") {
            info_window_string += "<p class='web'>" + v.titlewebsite + 
                ": <a href='http://" + v.website + "' target='_blank'>http://" + v.website + "</a></p>";
        } else {
            info_window_string += "<p class='web'>" + v.titlewebsite + 
                ": <a href='" + v.website + "' target='_blank'>" + v.website + "</a></p>";
        }
    }

	if(v.description != '') {
		info_window_string += "<p class='description'>"+v.description+"</p>";
	}
	
	
	if(v.cat_img != '') {
	    info_window_string += "<div class='products'><img src='"+v.cat_img+"' style='max-width:15px; max-height:15px;' /> "+v.cat_name+"</div>";
	}
	
	
    info_window_string += "<span class='email'><center><a href='/store/"+v.store_id+"' target='_blank' class='contact-clinic button blue-button' style='display:block;"+
                    "padding:5px 10px;"+
                    "margin-top:10px;"+ 
                    "margin-bottom:10px;"+
                    "margin-left:3px;"+
                    "border:1px solid #8b8b8b;"+
                    "text-align: center;"+
                    "font-weight:bold;"+
                    "width:190px;'>Ver detalle</a></center></span>";
					  

	// info_window_string += "<a href='javascript:streetView("+v.lat+","+v.lng+");'>"+ssf_street_view+"</a> | <a href='javascript:zoomHere("+v.lat+","+v.lng+");'>"+ssf_zoom_here+"</a> | <a href='javascript:direction(\""+v.address+"\","+v.lat+","+v.lng+");'>"+ssf_get_direction+"</a>";
	info_window_string += "</div>";

return info_window_string;
}
function toggleBounce(marker) {

	$(markers).each(function(i,marker2){
	
	 if(marker['__gm_id']!=marker2['__gm_id']){
	  marker2.setAnimation(null);
	  }

	});

	if (marker.getAnimation() != null) {
	  marker.setAnimation(null);
	} else {
	  marker.setAnimation(google.maps.Animation.BOUNCE);
	}
	
	var $allVideos = $("iframe[src^='http']");

					$allVideos.each(function() {

					$(this)
						.data('aspectRatio', this.height / this.width)
						.removeAttr('height')
						.removeAttr('width');

					});
				
					var newWidth = "220px";
				
					$allVideos.each(function() {

						var $el = $(this);
						$el
							.width(newWidth)
							.height(newWidth);
					});
}