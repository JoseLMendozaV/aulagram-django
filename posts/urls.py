from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.home, name="home"),
    path("feed/", views.feed, name="feed"),
    path("publicar/", views.post_create, name="create"),
    path("publicacion/<int:pk>/", views.post_detail, name="detail"),
    path("publicacion/<int:pk>/editar/", views.post_edit, name="edit"),
    path("publicacion/<int:pk>/eliminar/", views.post_delete, name="delete"),
    path("publicacion/<int:pk>/like/", views.toggle_like, name="like"),
    path("publicacion/<int:pk>/comentar/", views.comment_create, name="comment"),
    path("comentario/<int:pk>/eliminar/", views.comment_delete, name="comment_delete"),
]
