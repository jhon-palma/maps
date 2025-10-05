from django.urls import path
from apps.accounts.views import accounts


urlpatterns = [
    path("login/", accounts.login_view, name="login"),
    path("logout/", accounts.logout_view, name="logout"),
    
    path("users/", accounts.users_list, name="users_list"),
    path("users/create/", accounts.create_user, name="create_user"),
    path("users/<int:user_id>/edit/", accounts.edit_user, name="edit_user"),
    path("users/<int:user_id>/delete/", accounts.delete_user, name="delete_user"),
    path('users/<int:user_id>/reset-password/', accounts.reset_user_password, name='reset_user_password'),

]
