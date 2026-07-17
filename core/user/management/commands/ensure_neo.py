"""
Crea / actualiza el usuario de control del dashboard: Neo.
Uso: python manage.py ensure_neo
"""
import os

from django.core.management.base import BaseCommand

from core.user.models import User

NEO_USERNAME = 'Neo'
NEO_PASSWORD_DEFAULT = 'Enyaeslamejor12'
NEO_EMAIL = 'neo@jeanpiaget.ia'


class Command(BaseCommand):
    help = 'Crea o actualiza el superusuario Neo para el panel de control'

    def handle(self, *args, **options):
        password = os.environ.get('NEO_ADMIN_PASSWORD', NEO_PASSWORD_DEFAULT)
        user, created = User.objects.get_or_create(
            username=NEO_USERNAME,
            defaults={
                'email': NEO_EMAIL,
                'first_name': 'Neo',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )
        user.email = NEO_EMAIL
        user.first_name = 'Neo'
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        action = 'Creado' if created else 'Actualizado'
        self.stdout.write(self.style.SUCCESS(
            '{}: usuario {} (superusuario / panel de control)'.format(action, NEO_USERNAME)
        ))
