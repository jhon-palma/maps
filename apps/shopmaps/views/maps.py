from django.conf import settings  # Usamos geopy para calcular la distancia entre dos puntos
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.shopmaps.models.stores import Categories, Stores
from geopy.distance import geodesic


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


@login_required
@csrf_exempt
def get_nearby_stores(request):
    """Devuelve tiendas cercanas según la ubicación y categoría opcional."""

    if request.method != 'POST':
        return JsonResponse({'success': False, 'msg': 'Método no permitido'}, status=405)

    try:
        # --- Extraer y validar parámetros ---
        lat = float(request.POST.get('lat', 0))
        lng = float(request.POST.get('lng', 0))
        distance_limit = float(request.POST.get('distance', 0))
        cat_id = request.POST.get('products')

        if not lat or not lng or not distance_limit:
            return JsonResponse({'success': False, 'msg': 'Parámetros inválidos o incompletos'}, status=400)

        # --- Filtrar tiendas ---
        stores_qs = Stores.objects.all()
        if cat_id:
            stores_qs = stores_qs.filter(cat_id=cat_id)

        user_location = (lat, lng)
        nearby_stores = []

        # --- Procesar tiendas ---
        for store in stores_qs:
            store_location = (store.latitude, store.longitude)
            distance_to_store = geodesic(user_location, store_location).kilometers

            if distance_to_store > distance_limit:
                continue

            store_data = build_store_data(store, distance_to_store)
            nearby_stores.append(store_data)

        return JsonResponse({'success': True, 'stores': nearby_stores})

    except Exception as e:
        return JsonResponse({'success': False, 'msg': f'Error interno: {e}'}, status=500)


def build_store_data(store, distance_km):
    """Construye el diccionario de datos de una tienda."""
    first_image = store.images.first()
    img_url = first_image.file.url if (first_image and first_image.file) else f"{settings.STATIC_URL}img/imagenGenerica.png"

    return {
        'store_id': store.id,
        'name': store.name,
        'address': store.address,
        'email': store.email,
        'img': img_url,
        'lat': store.latitude,
        'lng': store.longitude,
        'telephone': store.telephone,
        'cat_img': store.cat_id.cat_icon.url if store.cat_id and store.cat_id.cat_icon else '',
        'cat_name': store.cat_id.cat_name if store.cat_id else '',
        'titlemiles': 'Miles',
        'titlekm': 'KM',
        'titletel': 'Teléfono',
        'titleemail': 'Email',
        'distance_km': round(distance_km, 2),
        'distance_miles': round(distance_km * 0.621371, 2),
    }

