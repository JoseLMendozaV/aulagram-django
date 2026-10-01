from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProfileForm, RegisterForm, RoleUpdateForm, UserUpdateForm
from .models import User


def register(request):
    if request.user.is_authenticated:
        return redirect("posts:feed")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Tu cuenta fue creada. Completa ahora tu perfil.")
        return redirect("accounts:profile_edit")
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile_detail(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.select_related("author__profile").all()
    return render(
        request,
        "accounts/profile_detail.html",
        {"profile_user": profile_user, "posts": posts},
    )


@login_required
@transaction.atomic
def profile_edit(request):
    user_form = UserUpdateForm(request.POST or None, instance=request.user)
    profile_form = ProfileForm(
        request.POST or None, request.FILES or None, instance=request.user.profile
    )
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, "Perfil actualizado correctamente.")
        return redirect("accounts:profile", username=request.user.username)
    return render(
        request,
        "accounts/profile_edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def is_admin(user):
    return user.is_authenticated and user.can_manage_users


@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.select_related("profile").order_by("username")
    return render(request, "accounts/user_list.html", {"users": users})


@require_POST
@user_passes_test(is_admin)
def user_role_update(request, pk):
    target = get_object_or_404(User, pk=pk)
    if target.is_superuser:
        messages.error(request, "No se puede cambiar el rol de un superusuario.")
        return redirect("accounts:user_list")
    form = RoleUpdateForm(request.POST, instance=target)
    if form.is_valid():
        form.save()
        messages.success(request, f"Rol de @{target.username} actualizado.")
    else:
        messages.error(request, "El rol indicado no es valido.")
    return redirect("accounts:user_list")
