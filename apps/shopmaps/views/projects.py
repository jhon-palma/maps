from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from apps.shopmaps.forms.project import ProjectForm
from apps.shopmaps.models.stores import Project

# Vista para listar las categorías
def project_list(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
        'title': "Proyectos",
        'module_name':'Tiendas',
        'section': 'Proyectos',
        'list_url': reverse_lazy('maps:projects_list'),
        'group': 'Listado de Proyectos',
    }
    return render(request, 'projects/list.html', context)

# Vista para crear una nueva categoría
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maps:projects_list')  # Redirige a la lista de categorías
    else:
        form = ProjectForm()
    context = {
        'form': form,
        'title': "Proyectos",
        'module_name':'Tiendas',
        'section': 'Proyectos de Tiendas',
        'list_url': reverse_lazy('maps:projects_list'),
        'group': 'Crear categoria',
    }
    return render(request, 'projects/form.html', context)

# Vista para editar una categoría
def project_edit(request, pk):
    category = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('maps:projects_list')  # Redirige a la lista de categorías
    else:
        form = ProjectForm(instance=category)
    context = {
        'form': form,
        'title': "Proyectos",
        'module_name':'Tiendas',
        'section': 'Proyectos de Tiendas',
        'list_url': reverse_lazy('maps:projects_list'),
        'group': 'Editar categoria',
    }
    return render(request, 'projects/form.html', context)

# Vista para eliminar una categoría
def project_delete(request, pk):
    category = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('projects_list')  # Redirige a la lista de categorías
    return render(request, 'mi_app/category_confirm_delete.html', {'category': category})
