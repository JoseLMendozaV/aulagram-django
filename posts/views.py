from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from .forms import CommentForm, PostForm
from .models import Comment, Like, Post


def post_queryset():
    """Consulta comun para evitar N+1 en el feed y el detalle."""
    return (
        Post.objects.select_related("author__profile")
        .prefetch_related(
            Prefetch("comments", queryset=Comment.objects.select_related("user"))
        )
        .annotate(like_count=Count("likes", distinct=True))
    )


def wants_json(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def home(request):
    return redirect("posts:feed" if request.user.is_authenticated else "accounts:login")


@login_required
def feed(request):
    posts = post_queryset()
    liked_post_ids = set(
        Like.objects.filter(user=request.user, post__in=posts).values_list(
            "post_id", flat=True
        )
    )
    return render(
        request,
        "posts/feed.html",
        {"posts": posts, "liked_post_ids": liked_post_ids, "comment_form": CommentForm()},
    )


@login_required
def post_detail(request, pk):
    post = get_object_or_404(post_queryset(), pk=pk)
    liked_post_ids = {post.pk} if post.likes.filter(user=request.user).exists() else set()
    return render(
        request,
        "posts/post_detail.html",
        {"post": post, "liked_post_ids": liked_post_ids, "comment_form": CommentForm()},
    )


@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Publicacion creada.")
        return redirect("posts:detail", pk=post.pk)
    return render(request, "posts/post_form.html", {"form": form, "title": "Nueva publicacion"})


def can_change_post(user, post):
    return (
        user == post.author
        or user.can_manage_users
        or user.has_perm("posts.moderate_post")
    )


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        raise PermissionDenied("Solo el autor puede editar esta publicacion.")
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Publicacion actualizada.")
        return redirect("posts:detail", pk=post.pk)
    return render(request, "posts/post_form.html", {"form": form, "title": "Editar publicacion"})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not can_change_post(request.user, post):
        raise PermissionDenied("No tienes permiso para eliminar esta publicacion.")
    if request.method == "POST":
        post.delete()
        messages.success(request, "Publicacion eliminada.")
        return redirect("posts:feed")
    return render(request, "posts/post_confirm_delete.html", {"post": post})


@require_POST
@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    if wants_json(request):
        return JsonResponse({"liked": created, "count": post.likes.count()})
    return redirect(request.POST.get("next") or "posts:feed")


@require_POST
@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
        if wants_json(request):
            html = render_to_string(
                "posts/_comment.html",
                {"comment": comment, "post": post},
                request=request,
            )
            return JsonResponse({"html": html, "comment_id": comment.pk})
    else:
        if wants_json(request):
            error = form.errors.get("body", ["No se pudo publicar el comentario."])[0]
            return JsonResponse({"error": str(error)}, status=422)
        messages.error(request, "El comentario esta vacio o es demasiado largo.")
    return redirect("posts:feed")


@require_POST
@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment.objects.select_related("post"), pk=pk)
    if not (
        request.user == comment.user
        or request.user == comment.post.author
        or request.user.can_manage_users
    ):
        raise PermissionDenied("No tienes permiso para eliminar este comentario.")
    comment.delete()
    if wants_json(request):
        return JsonResponse({"deleted": True})
    messages.success(request, "Comentario eliminado.")
    return redirect("posts:feed")
