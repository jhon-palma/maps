from django.db.models import ProtectedError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from config.decorators.role_required import role_required
from apps.shopmaps.forms.project import ProjectForm
from apps.shopmaps.models.stores import Project


@role_required(["admin"])
def project_list(request):
    """Muestra el listado de proyectos creados."""
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


@role_required(["admin"])
def project_create(request):
    """Muestra el listado de proyectos creados."""
    form = ProjectForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Proyecto creado correctamente.")
        return redirect('maps:projects_list')

    context = {
        'form': form,
        'title': "Proyectos",
        'module_name':'Tiendas',
        'section': 'Proyectos de Tiendas',
        'list_url': reverse_lazy('maps:projects_list'),
        'group': 'Crear categoria',
    }
    return render(request, 'projects/form.html', context)


@role_required(["admin"])
def project_edit(request, pk):
    """Edita un proyecto existente."""
    proyect = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=proyect)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Proyecto actualizado correctamente.")
        return redirect('maps:projects_list')

    context = {
        'form': form,
        'title': "Proyectos",
        'module_name':'Tiendas',
        'section': 'Proyectos de Tiendas',
        'list_url': reverse_lazy('maps:projects_list'),
        'group': 'Editar proyecto',
    }
    return render(request, 'projects/form.html', context)


@role_required(["admin"])
def project_delete(request, pk):
    """Elimina un proyecto si no tiene tiendas asociadas."""
    proyect = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        try:
            proyect.delete()
            messages.success(request, "Proyecto eliminado correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar: hay tiendas asociadas a este proyecto.")
        return redirect('maps:projects_list')
    
    context = {
        'object': proyect,
        'title': "Proyectos",
        'module_name':'Tiendas',
        'section': 'Proyectos de Tiendas',
        'list_url': reverse_lazy('maps:projects_list'),
        'group': 'Eliminar proyecto',
    }
    return render(request, 'projects/delete.html', context)
