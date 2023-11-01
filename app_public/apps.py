from django.apps import AppConfig


class AppAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_admin'

# lisasin, ei tea kas correct, vb vaja remove
class AppPublic(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_public'

