from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from apps.shopmaps.forms.categories import CategoryForm
from apps.shopmaps.models.stores import Categories

# Vista para listar las categorías
def category_list(request):
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

# Vista para crear una nueva categoría
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maps:category_list')  # Redirige a la lista de categorías
    else:
        form = CategoryForm()
    context = {
        'form': form,
        'title': "Categorias",
        'module_name':'Tiendas',
        'section': 'Categorias de Tiendas',
        'list_url': reverse_lazy('maps:category_list'),
        'group': 'Crear categoria',
    }
    return render(request, 'categories/form.html', context)

# Vista para editar una categoría
def category_edit(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('maps:category_list')  # Redirige a la lista de categorías
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'title': "Categorias",
        'module_name':'Tiendas',
        'section': 'Categorias de Tiendas',
        'list_url': reverse_lazy('maps:category_list'),
        'group': 'Editar categoria',
    }
    return render(request, 'categories/form.html', context)

# Vista para eliminar una categoría
def category_delete(request, pk):
    category = get_object_or_404(Categories, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')  # Redirige a la lista de categorías
    return render(request, 'mi_app/category_confirm_delete.html', {'category': category})
