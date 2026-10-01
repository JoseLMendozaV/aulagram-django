from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("registro/", views.register, name="register"),
    path(
        "iniciar-sesion/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("cerrar-sesion/", auth_views.LogoutView.as_view(), name="logout"),
    path("perfil/editar/", views.profile_edit, name="profile_edit"),
    path("perfil/<str:username>/", views.profile_detail, name="profile"),
    path("usuarios/", views.user_list, name="user_list"),
    path("usuarios/<int:pk>/rol/", views.user_role_update, name="role_update"),
]
