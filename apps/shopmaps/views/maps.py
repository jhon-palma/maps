from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.shopmaps.models.stores import Categories, Stores
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from geopy.distance import geodesic  # Usamos geopy para calcular la distancia entre dos puntos

@login_required
def index(request):
    """Página de inicio"""
    context = {
        'title': "ACE Shops",
        'module_name':'Tiendas',
        'section': 'Inicio',
        'group': 'Inicio',
    }
    return render(request, 'maps/index.html', context)


@login_required
def maps(request):
    """Mapa general con las tiendas"""
    categories = Categories.objects.all()
    context = {
        'title': "ACE Shops",
        'module_name':'Tiendas',
        'section': 'Inicio',
        'group': 'Inicio',
        'city' : "Los Ángeles, US",
        'country' : "Estados Unidos",
        'categories': categories,
    }
    return render(request, 'maps/maps.html', context)



@csrf_exempt
def get_nearby_stores(request):
    if request.method == 'POST':
        try:
            distance = float(request.POST.get('distance', 0))
            lat = float(request.POST.get('lat', 0))
            lng = float(request.POST.get('lng', 0))
            products = request.POST.get('products', '')

            stores = Stores.objects.all()  # Aquí puedes filtrar por productos si es necesario
            nearby_stores = []
            
            for store in stores:
                store_location = (store.latitude, store.longitude)
                user_location = (lat, lng)
                
                distance_to_store = geodesic(user_location, store_location)  # En kilómetros
                distance_km = distance_to_store.kilometers
                distance_miles = distance_to_store.miles
                
                if distance_to_store <= distance:
                    store_data = {
                        'name': store.name,
                        'address': store.address,
                        'lat': store.latitude,
                        'lng': store.longitude,
                        'category': store.cat_id.cat_name if store.cat_id else '',
                    }
                    nearby_stores.append(store_data)
                # print("###############")
                # print(f"nearby_stores: ",nearby_stores)
                # print("###############")

            nearby_stores = nearby_stores[:10]

            return JsonResponse({
                'success': True,
                'stores': nearby_stores,
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'msg': str(e)
            })

    return JsonResponse({
        'success': False,
        'msg': 'Invalid request method'
    })
