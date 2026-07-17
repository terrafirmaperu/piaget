# Generated manually — Inscritos (antes PerfilAlumno)

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Usuario (control)', 'verbose_name_plural': 'Usuarios (control)'},
        ),
        migrations.CreateModel(
            name='Inscrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=120, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=120, verbose_name='Apellidos')),
                ('celular', models.CharField(max_length=20, verbose_name='Celular')),
                ('lugar_nacimiento', models.CharField(max_length=150, verbose_name='Lugar de nacimiento')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1, verbose_name='Género')),
                ('edad', models.PositiveSmallIntegerField(verbose_name='Edad')),
                ('padre_nombres', models.CharField(max_length=120, verbose_name='Nombres del padre')),
                ('padre_apellidos', models.CharField(max_length=120, verbose_name='Apellidos del padre')),
                ('padre_celular', models.CharField(max_length=20, verbose_name='Celular del padre')),
                ('madre_nombres', models.CharField(max_length=120, verbose_name='Nombres de la madre')),
                ('madre_apellidos', models.CharField(max_length=120, verbose_name='Apellidos de la madre')),
                ('madre_celular', models.CharField(max_length=20, verbose_name='Celular de la madre')),
                ('activo', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Inscrito el')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inscrito', to=settings.AUTH_USER_MODEL, verbose_name='Cuenta de acceso')),
            ],
            options={
                'verbose_name': 'Inscrito',
                'verbose_name_plural': 'Inscritos',
                'ordering': ['-created_at'],
            },
        ),
    ]
