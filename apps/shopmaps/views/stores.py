from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geoip2 import GeoIP2
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView

from apps.shopmaps.forms.stores import ImageFormSet, StoreForm
from apps.shopmaps.models.stores import Images, StoreProject, Stores
from config.decorators.role_required import role_required


@role_required(["admin", "operador", "cliente"])
def store_list(request):
    """
    Vista para listar tiendas.
    Accesible por admin, operador y cliente.
    """
    stores = Stores.objects.all().order_by('code')
    context = {
        'title': "Tiendas",
        'module_name':'Tiendas',
        'section': 'Tiendas',
        'list_url': reverse_lazy('maps:stores_list'),
        'group': 'Listado de Tiendas',
    }
    return render(request, 'stores/list.html', context)


@role_required(["admin", "operador", "cliente"])
def store_list_json(request):
    """
    Vista AJAX para DataTables (server-side processing).
    Accesible por admin, operador y cliente.
    Retorna datos paginados y filtrados en formato JSON.
    """
    try:
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "")

        stores = Stores.objects.all().select_related("city", "city__state", "cat_id").order_by("code")

        if search_value:
            stores = stores.filter(
                Q(name__icontains=search_value) |
                Q(address__icontains=search_value) |
                Q(city__name__icontains=search_value) |
                Q(code__icontains=search_value)
            )

        total = stores.count()

        paginator = Paginator(stores, length)
        page_number = start // length + 1
        page_obj = paginator.get_page(page_number)

        user_role = getattr(request.user, "role", None)
        can_edit = user_role in ["admin", "operador"]

        data = []
        for store in page_obj:
            actions = f"""
                <div class='btn-group'>
                    <a href='/store/{store.pk}/' class='btn btn-sm btn-outline-primary'>
                        <i class='bi bi-search'></i>
                    </a>
            """

            if can_edit:
                actions += f"""
                    <a href='/store/{store.pk}/edit/' class='btn btn-sm btn-outline-warning'>
                        <i class='bi bi-pencil-square'></i>
                    </a>
                """

            actions += "</div>"
            data.append({
                "code": store.code,
                "name": store.name,
                "address": store.address,
                "city": str(store.city),
                "state": str(store.city.state),
                "created": store.created.strftime("%Y-%m-%d"),
                "category": str(store.cat_id),
                "status_store": store.status_store,
                "actions": actions,
            })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({
        "draw": draw,
        "recordsTotal": total,
        "recordsFiltered": total,
        "data": data,
    })


@role_required(["admin", "operador"])
def store_create(request):
    """Vista para crear tiendas."""
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


@role_required(["admin", "operador"])
def store_edit(request, pk):
    """Vista para editar tiendas."""
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


@role_required(["admin"])
def store_delete(request, pk):
    """Elimina una tienda."""
    store = get_object_or_404(Stores, pk=pk)
    if request.method == 'POST':
        store.delete()
        return redirect('store_list')
    return render(request, 'mi_app/store_confirm_delete.html', {'store': store})


@login_required
def get_client_ip(request):
    """Devuelve la dirección IP del cliente. Usado y requerido en el js del maps."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class StoreDetailView(LoginRequiredMixin, DetailView):
    """Vista de detalle de tienda (acceso restringido a admin, operador y cliente)."""
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

        next_store = (
            Stores.objects.filter(code__gt=store.code)
            .order_by("code")
            .first()
        )

        context["prev_store"] = prev_store
        context["next_store"] = next_store

        return context
