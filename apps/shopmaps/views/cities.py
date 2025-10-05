from django.http import JsonResponse

from apps.shopmaps.models.stores import City
from config.decorators.role_required import role_required


@role_required(["admin", "operador"])
def load_cities(request):
    """
    Devuelve un listado JSON de ciudades filtradas por estado.
    Requiere autenticación y permisos de admin u operador.
    """
    state_id = request.GET.get("state_id")

    if not state_id:
        return JsonResponse(
            {"error": "El parámetro 'state_id' es obligatorio."},
            status=400
        )
    
    cities = City.objects.filter(state_id=state_id).order_by("name")

    if not cities.exists():
        return JsonResponse(
            {"message": "No se encontraron ciudades para el estado seleccionado."},
            status=404
        )

    data = list(cities.values("id", "name"))
    return JsonResponse(data, safe=False, status=200)