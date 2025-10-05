from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import ProtectedError
from apps.accounts.forms.users import AdminUserChangeForm, AdminUserCreationForm
from apps.accounts.models.accounts import CustomUser
from django.urls import reverse


def login_view(request):
    """
    Vista de autenticación de usuarios.
    Redirige según el rol del usuario.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == "admin":
                return redirect(reverse("maps:stores_dashboard"))
            else:
                return redirect(reverse("maps:index"))
        
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    
    context = {
        'title': "Ingresar",
    }
    return render(request, "accounts/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def users_list(request):
    usuarios = CustomUser.objects.all().order_by("-modified")
    context = {
        'title': "Usuarios",
        'module_name':'Usuarios',
        'section': 'Listado usuarios',
        'group': 'Listado usuarios',
        "usuarios": usuarios,
    }
    return render(request, "accounts/list.html", context)

@login_required
def create_user(request):
    # Solo un administrador puede crear usuarios
    # if request.user.role != "admin":
    #     return HttpResponseForbidden("No tienes permiso para crear usuarios")

    if request.method == "POST":
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Usuario creado correctamente.") 
            return redirect("users_list")
        else:
            messages.error(request, "❌ Hubo un error al crear el usuario. Verifica los campos.")
    else:
        form = AdminUserCreationForm()
    
    context = {
        'title': "Crear Usuario",
        'module_name':'Usuarios',
        'section': 'Crear usuario',
        'group': 'Crear usuario',
        "form": form,
        "action" : "add",
    }
    return render(request, "accounts/form.html", context)

@login_required
def edit_user(request, user_id):
    # if request.user.role != "admin":
    #     return HttpResponseForbidden("No tienes permiso para editar usuarios")

    user_obj = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        form = AdminUserChangeForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Usuario modificado correctamente.") 
            return redirect("users_list")
        else:
            messages.error(request, "❌ Hubo un error al editar el usuario. Verifica los campos.")
    else:
        form = AdminUserChangeForm(instance=user_obj)

    context = {
        'title': "Editar Usuario",
        'module_name':'Usuarios',
        'section': 'Editar usuario',
        'group': 'Editar usuario',
        "form": form,
        "action" : "edit",
        "user_obj": user_obj
    }
    return render(request, "accounts/form.html", context)

@login_required
def delete_user(request, user_id):
    if request.user.role != "admin":
        return HttpResponseForbidden("No tienes permiso para eliminar usuarios")

    user_obj = get_object_or_404(CustomUser, id=user_id)

    try:
        user_obj.delete()
        messages.success(request, "✅ Usuario eliminado correctamente.")
    except ProtectedError:
        messages.error(request, "❌ No se puede eliminar este usuario porque tiene datos asociados (ejemplo: tiendas creadas).")

    return redirect("users_list")