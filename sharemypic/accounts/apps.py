from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sharemypic.accounts"

    def ready(self) -> None:
        import sharemypic.accounts.signals