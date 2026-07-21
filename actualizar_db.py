"""Crea las tablas para poder guardar inscritos."""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.core.management import call_command

call_command('migrate', interactive=False, verbosity=2)
call_command('ensure_neo', verbosity=1)
call_command('ensure_alumno', verbosity=1)
print('OK — detén runserver (Ctrl+C), vuelve a levantarlo y guarda el registro otra vez.')
