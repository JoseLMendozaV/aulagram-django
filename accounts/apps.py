from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Registra las senales que crean el perfil junto con el usuario.
        import accounts.signals  # noqa: F401
