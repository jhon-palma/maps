from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):
    """
    Decorador para restringir acceso según el rol del usuario.
    Redirige a 'login' si no está autenticado o a 'sin_permiso' si no tiene acceso.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")  # o la ruta que uses para login

            if request.user.role not in allowed_roles:
                # Puedes redirigir o lanzar un error 403
                return redirect("maps:index")  # crea una vista/template 'sin_permiso.html'
                # raise PermissionDenied("No tienes permiso para acceder a esta vista")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator