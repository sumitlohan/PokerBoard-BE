from django.apps import AppConfig

class UserConfig(AppConfig):
    name = 'apps.user'
    def ready(self) -> None:
        import apps.user.signals
        return super().ready()
