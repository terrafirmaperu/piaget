"""
Crea / actualiza un inscrito de prueba para Sin limites.
Uso: python manage.py ensure_alumno
"""
from datetime import date

from django.core.management.base import BaseCommand

from core.user.models import Inscrito, User

ALUMNO_USERNAME = 'alumno'
ALUMNO_PASSWORD = 'Alumno123'


class Command(BaseCommand):
    help = 'Crea o actualiza el inscrito de prueba "alumno" para Sin limites'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username=ALUMNO_USERNAME,
            defaults={
                'first_name': 'Ana',
                'last_name': 'Pérez',
                'email': 'alumno@jeanpiaget.ia',
                'is_staff': False,
                'is_superuser': False,
                'is_active': True,
            },
        )
        user.first_name = 'Ana'
        user.last_name = 'Pérez'
        user.email = 'alumno@jeanpiaget.ia'
        user.is_staff = False
        user.is_superuser = False
        user.is_active = True
        user.set_password(ALUMNO_PASSWORD)
        user.save()

        inscrito, inscrito_created = Inscrito.objects.get_or_create(
            user=user,
            defaults={
                'nombres': 'Ana',
                'apellidos': 'Pérez',
                'celular': '0999999999',
                'lugar_nacimiento': 'Quito',
                'fecha_nacimiento': date(2015, 5, 10),
                'genero': Inscrito.GENERO_FEMENINO,
                'edad': Inscrito.calcular_edad(date(2015, 5, 10)) or 10,
                'padre_nombres': 'Carlos',
                'padre_apellidos': 'Pérez',
                'padre_celular': '0988888888',
                'madre_nombres': 'María',
                'madre_apellidos': 'López',
                'madre_celular': '0977777777',
                'activo': True,
            },
        )
        if not inscrito_created:
            inscrito.nombres = 'Ana'
            inscrito.apellidos = 'Pérez'
            inscrito.activo = True
            inscrito.save(update_fields=['nombres', 'apellidos', 'activo', 'updated_at'])

        action = 'Creado' if created or inscrito_created else 'Actualizado'
        self.stdout.write(self.style.SUCCESS(
            '{}: usuario {} / {} (inscrito Sin limites)'.format(
                action, ALUMNO_USERNAME, ALUMNO_PASSWORD
            )
        ))
