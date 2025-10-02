from django.http import JsonResponse

from apps.shopmaps.models.stores import City


def load_cities(request):
    state_id = request.GET.get("state_id")
    cities = City.objects.filter(state_id=state_id).order_by("name")
    return JsonResponse(list(cities.values("id", "name")), safe=False)