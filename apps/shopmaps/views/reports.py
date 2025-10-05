from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.utils.timezone import now
import csv
from django.http import HttpResponse
from django.utils import timezone

from apps.shopmaps.models.stores import Stores
from config.decorators.role_required import role_required


@role_required(["admin"])
def stores_dashboard(request):
    """Vista para mostrar los diferentes reportes en el dashboard"""
    # 1️⃣ Cantidad de imágenes por tipo
    image_counts = {
        'image': Stores.objects.exclude(image="0").count(),
        'image1': Stores.objects.exclude(image1="0").count(),
        'image2': Stores.objects.exclude(image2="0").count(),
        'image3': Stores.objects.exclude(image3="0").count(),
        'image4': Stores.objects.exclude(image4="0").count(),
    }

    # 2️⃣ Cantidad de tiendas por ciudad
    stores_by_city = (
        Stores.objects.values('city__name')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]  # solo las 10 con más tiendas
    )

    # 3️⃣ Tiendas por categoria
    stores_by_category = (
        Stores.objects.values('cat_id__cat_name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    
    # 4️⃣ Tiendas últimos 5 días
    last_five_days = now() - timedelta(days=5)

    stores_by_day = (
        Stores.objects.filter(created__gte=last_five_days)
        .annotate(day=TruncDate('created'))
        .values('day')
        .annotate(total=Count('id'))
        .order_by('day')
    )

    context = {
        'title': 'Dashboard',
        'module_name':'Tiendas',
        'section': 'Dashboard',
        'group': 'Dashboard',
        'image_counts': image_counts,
        'stores_by_city': stores_by_city,
        'stores_by_category': stores_by_category,
        'stores_by_day': list(stores_by_day),
    }
    return render(request, 'reports/dashboard.html', context)


@role_required(["admin"])
def reports(request):
    context = {
        'title': 'Reportes',
        'module_name':'Tiendas',
        'section': 'Reportes',
        'group': 'Reportes',
    }
    return render(request, 'reports/reports.html', context)


@role_required(["admin"])
def report_general_csv(request):
    """
    Genera un reporte CSV con la lista de tiendas registradas.
    """
    # Definir el nombre del archivo con fecha actual
    filename = f"Stores_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Configurar la respuesta HTTP como descarga de archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Encabezados del CSV
    writer.writerow([
        "Código",
        "Nombre",
        "Dirección",
        "Ciudad",
        "Estado",
        "Código Postal",
        "Teléfono",
        "Email",
        "Descripción",
        "Latitud",
        "Longitud",
        "Categoría",
        "Creado por",
        "Fecha de creación",
        "Fecha de modificación",
        "Proyecto",
    ])

    # Obtener las tiendas (puedes agregar filtros según el rol)
    stores = Stores.objects.select_related('cat_id').all().order_by('id')

    # Escribir filas
    for store in stores:
        writer.writerow([
            store.code,
            store.name,
            store.address or "",
            store.city or "",
            store.city.state or "",
            store.zip_code or "",
            store.telephone or "",
            store.email or "",
            store.description or "",
            store.latitude or "",
            store.longitude or "",
            store.cat_id.cat_name if store.cat_id else "",
            store.created_by or "",
            store.created.strftime("%Y-%m-%d %H:%M:%S") if store.created else "",
            store.modified.strftime("%Y-%m-%d %H:%M:%S") if store.modified else "",
            "Banco Rural",
        ])

    return response
