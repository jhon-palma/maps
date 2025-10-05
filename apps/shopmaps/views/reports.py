from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.utils.timezone import now

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
