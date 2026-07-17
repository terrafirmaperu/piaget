import os

from django.db import connection


class EnsureDatabaseMiddleware:
    """
    En local: si faltan tablas (user_user, etc.), aplica migrate
    en la primera petición HTTP. Así el registro puede guardar.
    """

    _checked = False

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not EnsureDatabaseMiddleware._checked:
            EnsureDatabaseMiddleware._checked = True
            self._ensure()
        return self.get_response(request)

    def _ensure(self):
        try:
            tables = set(connection.introspection.table_names())
        except Exception:
            tables = set()

        if 'user_user' in tables and 'user_inscrito' in tables:
            return

        from django.core.management import call_command

        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.makedirs(os.path.join(base), exist_ok=True)
        call_command('migrate', interactive=False, verbosity=1)
        try:
            call_command('ensure_neo', verbosity=0)
        except Exception:
            pass
