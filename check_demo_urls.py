"""Comprueba que las rutas demo existen. Uso: python check_demo_urls.py"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.urls import reverse

for name, kwargs in (
    ('demo_opciones', None),
    ('demo_materia', {'slug': 'matematicas'}),
):
    try:
        url = reverse(name, kwargs=kwargs) if kwargs else reverse(name)
        print('OK', name, '->', url)
    except Exception as exc:
        print('FAIL', name, exc)
