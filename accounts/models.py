from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    """Usuario del proyecto con un rol sencillo para practicar permisos."""

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        CREATOR = "CREATOR", "Creador"
        MEMBER = "MEMBER", "Usuario"

    email = models.EmailField("correo electronico", unique=True)
    role = models.CharField(
        "rol", max_length=10, choices=Role.choices, default=Role.MEMBER
    )

    @property
    def can_manage_users(self):
        return self.is_superuser or self.role == self.Role.ADMIN

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)


class Skill(models.Model):
    """Catalogo estandarizado reutilizable entre perfiles (CR-10)."""

    name = models.CharField("nombre", max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "habilidad"
        verbose_name_plural = "habilidades"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField("foto de perfil", upload_to="profiles/", blank=True)
    bio = models.CharField("biografia", max_length=160, blank=True)
    location = models.CharField("ubicacion", max_length=80, blank=True)
    website = models.URLField("sitio web", blank=True)
    skills = models.ManyToManyField(Skill, verbose_name="habilidades", blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Create your models here.
