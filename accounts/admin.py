from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, Skill, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Rol educativo", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Datos", {"fields": ("email", "role")}),)
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location")
    search_fields = ("user__username", "bio")


admin.site.register(Skill)

# Register your models here.
