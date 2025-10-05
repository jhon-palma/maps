from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from apps.accounts.forms.users import AdminPasswordResetForm, AdminUserChangeForm, AdminUserCreationForm
from apps.accounts.models.accounts import CustomUser
from config.decorators.role_required import role_required


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


@role_required(["admin"])
def users_list(request):
    """
    Vista para ver listado de usuarios.
    """
    usuarios = CustomUser.objects.all().order_by("-modified")
    context = {
        'title': "Usuarios",
        'module_name':'Usuarios',
        'section': 'Listado usuarios',
        'group': 'Listado usuarios',
        "usuarios": usuarios,
    }
    return render(request, "accounts/list.html", context)


@role_required(["admin"])
def create_user(request):
    """
    Vista para crear usuarios.
    """
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


@role_required(["admin"])
def edit_user(request, user_id):
    """
    Vista para editar usuarios.
    """
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


@role_required(["admin"])
def delete_user(request, user_id):
    """
    Vista para eliminar usuarios.
    """
    user_obj = get_object_or_404(CustomUser, id=user_id)

    try:
        user_obj.delete()
        messages.success(request, "✅ Usuario eliminado correctamente.")
    except ProtectedError:
        messages.error(request, "❌ No se puede eliminar este usuario porque tiene datos asociados (ejemplo: tiendas creadas).")

    return redirect("users_list")


@role_required(["admin"])
def reset_user_password(request, user_id):
    """
    Permite a un administrador restablecer la contraseña de un usuario.
    """
    user_obj = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        form = AdminPasswordResetForm(user_obj, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"✅ Contraseña del usuario {user_obj.username} actualizada correctamente.")
            return redirect("users_list")
        else:
            messages.error(request, "❌ Hubo un error al actualizar la contraseña. Verifica los campos.")
    else:
        form = AdminPasswordResetForm(user_obj)

    context = {
        'title': "Restablecer Contraseña",
        'module_name': 'Usuarios',
        'section': f"Restablecer contraseña de {user_obj.username}",
        'group': 'Resetear contraseña',
        'form': form,
        'user_obj': user_obj,
    }

    return render(request, "accounts/password_reset.html", context)
