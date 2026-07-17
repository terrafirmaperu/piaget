# -*- coding: utf-8 -*-
import uuid
from datetime import date

from crum import get_current_request
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Cuenta de acceso.
    - Usuarios de control: is_staff / is_superuser (evalúan y administran).
    - Inscritos: tienen ficha Inscrito (Sin limites); no son control.
    """

    dni = models.CharField(max_length=13, unique=True, blank=True, null=True, verbose_name='Dni / documento')
    is_change_password = models.BooleanField(default=False)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True, default=uuid.uuid4, unique=True)

    def generate_token(self):
        return uuid.uuid4()

    def set_group_session(self):
        try:
            request = get_current_request()
            groups = request.user.groups.all()
            if groups and 'group' not in request.session:
                request.session['group'] = groups[0]
        except Exception:
            pass

    @property
    def es_control(self):
        """Usuario del sistema de control (evalúa / administra)."""
        return bool(self.is_staff or self.is_superuser)

    @property
    def es_inscrito(self):
        """Persona inscrita en Sin limites (no es control)."""
        return Inscrito.objects.filter(user_id=self.pk).exists()

    class Meta:
        app_label = 'user'
        verbose_name = 'Usuario (control)'
        verbose_name_plural = 'Usuarios (control)'

    def __str__(self):
        return self.get_full_name() or self.username


class Inscrito(models.Model):
    """
    Inscrito en Sin limites — datos personales + padres.
    Distinto de los usuarios de control del dashboard.
    """

    GENERO_MASCULINO = 'M'
    GENERO_FEMENINO = 'F'
    GENERO_CHOICES = (
        (GENERO_MASCULINO, 'Masculino'),
        (GENERO_FEMENINO, 'Femenino'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='inscrito',
        verbose_name='Cuenta de acceso',
    )

    nombres = models.CharField(max_length=120, verbose_name='Nombres')
    apellidos = models.CharField(max_length=120, verbose_name='Apellidos')
    celular = models.CharField(max_length=20, verbose_name='Celular')
    lugar_nacimiento = models.CharField(max_length=150, verbose_name='Lugar de nacimiento')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, verbose_name='Género')
    edad = models.PositiveSmallIntegerField(verbose_name='Edad')

    padre_nombres = models.CharField(max_length=120, verbose_name='Nombres del padre')
    padre_apellidos = models.CharField(max_length=120, verbose_name='Apellidos del padre')
    padre_celular = models.CharField(max_length=20, verbose_name='Celular del padre')

    madre_nombres = models.CharField(max_length=120, verbose_name='Nombres de la madre')
    madre_apellidos = models.CharField(max_length=120, verbose_name='Apellidos de la madre')
    madre_celular = models.CharField(max_length=20, verbose_name='Celular de la madre')

    activo = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Inscrito el')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'user'
        verbose_name = 'Inscrito'
        verbose_name_plural = 'Inscritos'
        ordering = ['-created_at']

    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)

    @property
    def nombre_completo(self):
        return '{} {}'.format(self.nombres, self.apellidos).strip()

    @staticmethod
    def calcular_edad(fecha_nacimiento):
        if not fecha_nacimiento:
            return None
        hoy = date.today()
        return hoy.year - fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
        )
