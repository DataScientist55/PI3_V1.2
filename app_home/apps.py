from django.apps import AppConfig

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_home'  # ✅ Certifique-se de que o nome bate com o de `INSTALLED_APPS`

