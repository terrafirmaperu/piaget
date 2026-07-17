from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password

from core.user.models import Inscrito, User

INPUT_CLASS = 'form-control'


def _attrs(placeholder, input_type='text', extra=None):
    attrs = {'class': INPUT_CLASS, 'placeholder': placeholder}
    if input_type != 'text':
        attrs['type'] = input_type
    if extra:
        attrs.update(extra)
    return attrs


class DatosPersonalesForm(forms.Form):
    nombres = forms.CharField(
        max_length=120,
        label='Nombres',
        widget=forms.TextInput(attrs=_attrs('Nombres', extra={'autofocus': True})),
    )
    apellidos = forms.CharField(
        max_length=120,
        label='Apellidos',
        widget=forms.TextInput(attrs=_attrs('Apellidos')),
    )
    celular = forms.CharField(
        max_length=20,
        label='Celular',
        widget=forms.TextInput(attrs=_attrs('Celular', 'tel')),
    )
    lugar_nacimiento = forms.CharField(
        max_length=150,
        label='Lugar de nacimiento',
        widget=forms.TextInput(attrs=_attrs('Lugar de nacimiento')),
    )
    fecha_nacimiento = forms.DateField(
        label='Fecha de nacimiento',
        widget=forms.DateInput(attrs=_attrs('Fecha de nacimiento', 'date', {'id': 'id_fecha_nacimiento'})),
    )
    genero = forms.ChoiceField(
        label='Género',
        choices=Inscrito.GENERO_CHOICES,
        widget=forms.Select(attrs={'class': INPUT_CLASS}),
    )
    edad = forms.IntegerField(
        label='Edad',
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(attrs=_attrs('Edad', 'number', {'id': 'id_edad', 'min': '1', 'max': '100'})),
    )


class DatosPadresForm(forms.Form):
    padre_nombres = forms.CharField(
        max_length=120,
        label='Nombres del padre',
        widget=forms.TextInput(attrs=_attrs('Nombres del padre', extra={'autofocus': True})),
    )
    padre_apellidos = forms.CharField(
        max_length=120,
        label='Apellidos del padre',
        widget=forms.TextInput(attrs=_attrs('Apellidos del padre')),
    )
    padre_celular = forms.CharField(
        max_length=20,
        label='Celular del padre',
        widget=forms.TextInput(attrs=_attrs('Celular del padre', 'tel')),
    )
    madre_nombres = forms.CharField(
        max_length=120,
        label='Nombres de la madre',
        widget=forms.TextInput(attrs=_attrs('Nombres de la madre')),
    )
    madre_apellidos = forms.CharField(
        max_length=120,
        label='Apellidos de la madre',
        widget=forms.TextInput(attrs=_attrs('Apellidos de la madre')),
    )
    madre_celular = forms.CharField(
        max_length=20,
        label='Celular de la madre',
        widget=forms.TextInput(attrs=_attrs('Celular de la madre', 'tel')),
    )


class CuentaForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='Usuario de acceso (inscrito)',
        widget=forms.TextInput(attrs=_attrs('Usuario de acceso', extra={'autocomplete': 'username', 'autofocus': True})),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs=_attrs('Contraseña', extra={'autocomplete': 'new-password'})),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs=_attrs('Confirmar contraseña', extra={'autocomplete': 'new-password'})),
    )

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Ese usuario ya existe. Elige otro.')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cleaned


class SinLimitesLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': INPUT_CLASS, 'placeholder': 'Usuario', 'autocomplete': 'username', 'autofocus': True}
        )
        self.fields['password'].widget.attrs.update(
            {'class': INPUT_CLASS, 'placeholder': 'Contraseña', 'autocomplete': 'current-password'}
        )
