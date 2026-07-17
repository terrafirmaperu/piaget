#!/usr/bin/env python
import os
import sys


def _migrar():
    base = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    import django
    django.setup()
    from django.core.management import call_command

    print('=== Actualizando base de datos ===')
    call_command('migrate', interactive=False, verbosity=1)
    try:
        call_command('ensure_neo', verbosity=1)
    except Exception as exc:
        print('Aviso ensure_neo:', exc)
    print('=== Base lista ===')


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # Antes de runserver: crea user_user, user_inscrito, etc.
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        if os.environ.get('RUN_MAIN') != 'true':
            try:
                _migrar()
            except Exception as exc:
                print('ERROR migrando:', exc)
                raise

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
