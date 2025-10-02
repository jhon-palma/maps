from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib.gis.geoip2 import GeoIP2
from django.views.generic import DetailView

from apps.shopmaps.forms.stores import ImageFormSet, StoreForm
from apps.shopmaps.models.stores import Images, StoreProject, Stores

# Vista para listar las tiendas
def store_list(request):
    stores = Stores.objects.all().order_by('code')  # Puedes filtrar o paginar si es necesario
    context = {
        'stores': stores,
        'title': "Tiendas",
        'module_name':'Tiendas',
        'section': 'Tiendas',
        'list_url': reverse_lazy('maps:stores_list'),
        'group': 'Listado de Tiendas',
    }
    return render(request, 'stores/list.html', context)

# Vista para crear una tienda
def store_create(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            print("FILES:", request.FILES)  
            print("FILES list:", request.FILES.getlist('images'))
            with transaction.atomic():
                store = form.save()
                for project in form.cleaned_data['projects']:
                    StoreProject.objects.create(store=store, project=project)

                formset.instance = store
                formset.save()

            return redirect('maps:stores_list')
    else:
        form = StoreForm()
        formset = ImageFormSet(queryset=Images.objects.none())

    g = GeoIP2()
    ip = get_client_ip(request)
    try:
        geo = g.city(ip)
        lat = geo["latitude"]
        lng = geo["longitude"]
        city_name = geo["city"]
        country_name = geo["country_name"]
    except:
        lat, lng = 4.60971, -74.08175
        city_name = "Bogotá"
        country_name = "Colombia"
    context = {
        'form': form,
        'formset': formset,
        'title': "Tiendas",
        'module_name':'Tiendas',
        'section': 'Tiendas',
        'list_url': reverse_lazy('maps:stores_list'),
        'group': 'Crear Tienda',
        'lat': lat,
        'lng': lng,
        'city': city_name,
        'country': country_name,
    }
    return render(request, 'stores/form.html', context)


def store_edit(request, pk):
    store = get_object_or_404(Stores, pk=pk)
    queryset = Images.objects.filter(store=store)
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        formset = ImageFormSet(request.POST, request.FILES, instance=store)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                store = form.save()
                formset.save()
            
            return redirect('maps:stores_list')
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", [f.errors for f in formset.forms])
    else:
        form = StoreForm(instance=store)
        formset = ImageFormSet(instance=store)
    
    lat, lng = store.latitude, store.longitude
    city_name = store.city
    country_name = "Estados Unidos"
    context = {
        'form': form,
        'formset': formset,
        'title': "Tiendas",
        'module_name':'Tiendas',
        'section': 'Tiendas',
        'list_url': reverse_lazy('maps:stores_list'),
        'group': 'Editar Tienda',
        'lat': lat,
        'lng': lng,
        'city': city_name,
        'country': country_name,
    }
    return render(request, 'stores/form.html', context)

# Vista para eliminar una tienda
def store_delete(request, pk):
    store = get_object_or_404(Stores, pk=pk)
    if request.method == 'POST':
        store.delete()
        return redirect('store_list')  # Redirige a la lista de tiendas
    return render(request, 'mi_app/store_confirm_delete.html', {'store': store})

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    print("################")
    print(ip)
    print("################")
    return ip


class StoreDetailView(DetailView):
    model = Stores
    template_name = "stores/store_detail.html"
    context_object_name = "store"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store = self.object
        context["title"] = "Detalle Tienda"
        context["module_name"] = 'Tiendas'
        context["section"] = 'Detalle Tienda'
        context["group"] = 'Detalle Tienda'
        context["detail"] = True
        context["images"] = store.images.all()
        context["city"] = store.city
        context["country"] = "Estados Unidos"
        context["list_url"] = reverse_lazy('maps:stores_list')
        prev_store = (
            Stores.objects.filter(code__lt=store.code)
            .order_by("-code")
            .first()
        )

        # 🔹 Buscar tienda siguiente por code
        next_store = (
            Stores.objects.filter(code__gt=store.code)
            .order_by("code")
            .first()
        )

        context["prev_store"] = prev_store
        context["next_store"] = next_store

        return context
