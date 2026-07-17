# # File: backend/apps/users/apps.py
# # AppConfig for users app (Developed by SAYAB)

# from django.apps import AppConfig

# class UsersConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "apps.users"

#     def ready(self):
#         # Import signals here if needed
#         try:
#             import apps.users.signals  # noqa
#         except Exception:
#             pass
# File: backend/apps/users/apps.py
# App config for users app (Developed by SAYAB)

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

    def ready(self):
        # import signals if any
        try:
            import apps.users.signals  # noqa
        except Exception:
            pass
