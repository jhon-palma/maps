from django.urls import path
from apps.shopmaps.views import cities, maps, stores, categories, projects
from django.conf import settings
from django.conf.urls.static import static

app_name = "maps"

urlpatterns = [
    path('', maps.index, name='index'),
    path('stores_list/', stores.store_list, name='stores_list'),  # Vista de lista
    path('create/', stores.store_create, name='store_create'),  # Vista para crear
    path('edit/<str:pk>/', stores.store_edit, name='store_edit'),  # Vista para editar
    path('delete/<str:pk>/', stores.store_delete, name='store_delete'),  # Vista para eliminar
    path("stores/<uuid:pk>/", stores.StoreDetailView.as_view(), name="store_detail"),

    # Categories
    path('categories/', categories.category_list, name='category_list'),  # Vista para listar
    path('categories/create/', categories.category_create, name='category_create'),  # Vista para crear
    path('categories/edit/<int:pk>/', categories.category_edit, name='category_edit'),  # Vista para editar
    path('categories/delete/<int:pk>/', categories.category_delete, name='category_delete'),  # Vista para eliminar

    # Projects
    path('projects/', projects.project_list, name='projects_list'),  # Vista para listar
    path('projects/create/', projects.project_create, name='project_create'),  # Vista para crear
    path('projects/edit/<int:pk>/', projects.project_edit, name='project_edit'),  # Vista para editar
    path('projects/delete/<int:pk>/', projects.project_delete, name='project_delete'),  # Vista para eliminar

    path("ajax/load-cities/", cities.load_cities, name="ajax_load_cities"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)