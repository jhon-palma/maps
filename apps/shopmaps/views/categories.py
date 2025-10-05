from django.db.models import ProtectedError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from config.decorators.role_required import role_required
from apps.shopmaps.forms.categories import CategoryForm
from apps.shopmaps.models.stores import Categories


@role_required(["admin"])
def category_list(request):
    """Muestra el listado de categorías de tiendas."""
    categories = Categories.objects.all()
    
    context = {
        'categories': categories,
        'title': "Categorias",
        'module_name':'Tiendas',
        'section': 'Categorias de Tiendas',
        'list_url': reverse_lazy('maps:categories_list'),
        'group': 'Listado de categorias',
    }
    return render(request, 'categories/list.html', context)


@role_required(["admin"])
def category_create(request):
    """Crea una nueva categoría de tienda."""
    form = CategoryForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoría creada correctamente.")
        return redirect('maps:category_list')
    
    context = {
        'form': form,
        'title': "Categorias",
        'module_name':'Tiendas',
        'section': 'Categorias de Tiendas',
        'list_url': reverse_lazy('maps:category_list'),
        'group': 'Crear categoria',
    }
    return render(request, 'categories/form.html', context)


@role_required(["admin"])
def category_edit(request, pk):
    """Edita una categoría existente."""
    category = get_object_or_404(Categories, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoría actualizada correctamente.")
        return redirect('maps:category_list')

    context = {
        'form': form,
        'title': "Categorias",
        'module_name':'Tiendas',
        'section': 'Categorias de Tiendas',
        'list_url': reverse_lazy('maps:category_list'),
        'group': 'Editar categoria',
    }
    return render(request, 'categories/form.html', context)


@role_required(["admin"])
def category_delete(request, pk):
    """Elimina una categoría si no tiene tiendas asociadas."""
    category = get_object_or_404(Categories, pk=pk)
    
    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, "Categoría eliminada correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar: hay tiendas asociadas a esta categoría.")
        return redirect('maps:category_list')
    
    context = {
        'object': category,
        'title': "Categorias",
        'module_name':'Tiendas',
        'section': 'Categorias de Tiendas',
        'list_url': reverse_lazy('maps:category_list'),
        'group': 'Eliminar categoria',
    }
    return render(request, 'categories/delete.html', context)
