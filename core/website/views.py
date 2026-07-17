from django.contrib import messages
from django.contrib.auth import login, logout
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, TemplateView

from core.user.models import Inscrito, User
from core.website.forms import (
    CuentaForm,
    DatosPadresForm,
    DatosPersonalesForm,
    SinLimitesLoginForm,
)

SESSION_PERSONAL = 'sin_limites_personal'
SESSION_PADRES = 'sin_limites_padres'


class HomeView(TemplateView):
    """Web pública — portada jean piaget IA."""

    template_name = 'website/home.html'


class SinLimitesView(View):
    """
    Experiencia "Sin limites" (solo inscritos).
    - Con sesión de inscrito: experiencia.
    - Sin sesión: registro.
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.es_inscrito:
                return render(
                    request,
                    'website/sin_limites.html',
                    {'title': 'Sin limites', 'inscrito': request.user.inscrito},
                )
            if request.user.es_control:
                return HttpResponseRedirect(reverse('dashboard'))
            logout(request)
        return HttpResponseRedirect(reverse('sin_limites_registro'))


class SinLimitesLoginView(FormView):
    """Ingreso de inscritos (ya tienen cuenta)."""

    template_name = 'website/sin_limites_login.html'
    form_class = SinLimitesLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.es_inscrito:
            return HttpResponseRedirect(reverse('sin_limites'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if not getattr(user, 'es_inscrito', False) and not Inscrito.objects.filter(user=user).exists():
            form.add_error(None, 'Esta cuenta no es de un inscrito. Usa Ingresar del menú si eres control.')
            return self.form_invalid(form)
        login(self.request, user)
        user.set_group_session()
        return HttpResponseRedirect(reverse('sin_limites'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sin limites'
        context['step'] = None
        return context


class RegistroPaso1View(FormView):
    """Paso 1 — datos personales del inscrito."""

    template_name = 'website/registro/paso1_personal.html'
    form_class = DatosPersonalesForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.es_inscrito:
            return HttpResponseRedirect(reverse('sin_limites'))
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return self.request.session.get(SESSION_PERSONAL, {})

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        data['fecha_nacimiento'] = data['fecha_nacimiento'].isoformat()
        self.request.session[SESSION_PERSONAL] = data
        self.request.session.modified = True
        return HttpResponseRedirect(reverse('sin_limites_registro_padres'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Datos personales', 'step': 1, 'total_steps': 3})
        return context


class RegistroPaso2View(FormView):
    """Paso 2 — datos de los padres."""

    template_name = 'website/registro/paso2_padres.html'
    form_class = DatosPadresForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.es_inscrito:
            return HttpResponseRedirect(reverse('sin_limites'))
        if SESSION_PERSONAL not in request.session:
            return HttpResponseRedirect(reverse('sin_limites_registro'))
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return self.request.session.get(SESSION_PADRES, {})

    def form_valid(self, form):
        self.request.session[SESSION_PADRES] = form.cleaned_data
        self.request.session.modified = True
        return HttpResponseRedirect(reverse('sin_limites_registro_cuenta'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Datos de los padres', 'step': 2, 'total_steps': 3})
        return context


class RegistroPaso3View(FormView):
    """Paso 3 — acceso del inscrito y guardado en base de datos."""

    template_name = 'website/registro/paso3_cuenta.html'
    form_class = CuentaForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.es_inscrito:
            return HttpResponseRedirect(reverse('sin_limites'))
        if SESSION_PERSONAL not in request.session or SESSION_PADRES not in request.session:
            return HttpResponseRedirect(reverse('sin_limites_registro'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        personal = self.request.session.get(SESSION_PERSONAL)
        padres = self.request.session.get(SESSION_PADRES)
        if not personal or not padres:
            return HttpResponseRedirect(reverse('sin_limites_registro'))

        # Asegura tablas antes de guardar (evita no such table: user_user).
        from django.core.management import call_command
        from django.db import connection

        try:
            tables = set(connection.introspection.table_names())
        except Exception:
            tables = set()
        if 'user_user' not in tables or 'user_inscrito' not in tables:
            call_command('migrate', interactive=False, verbosity=1)

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    first_name=personal['nombres'],
                    last_name=personal['apellidos'],
                    is_staff=False,
                    is_superuser=False,
                    is_active=True,
                )
                Inscrito.objects.create(
                    user=user,
                    nombres=personal['nombres'],
                    apellidos=personal['apellidos'],
                    celular=personal['celular'],
                    lugar_nacimiento=personal['lugar_nacimiento'],
                    fecha_nacimiento=personal['fecha_nacimiento'],
                    genero=personal['genero'],
                    edad=int(personal['edad']),
                    padre_nombres=padres['padre_nombres'],
                    padre_apellidos=padres['padre_apellidos'],
                    padre_celular=padres['padre_celular'],
                    madre_nombres=padres['madre_nombres'],
                    madre_apellidos=padres['madre_apellidos'],
                    madre_celular=padres['madre_celular'],
                    activo=True,
                )
        except Exception as exc:
            form.add_error(None, 'No se pudo guardar el inscrito: {}'.format(exc))
            return self.form_invalid(form)

        self.request.session.pop(SESSION_PERSONAL, None)
        self.request.session.pop(SESSION_PADRES, None)
        self.request.session.modified = True

        login(self.request, user)
        user.set_group_session()
        messages.success(self.request, 'Inscripción guardada. Bienvenido a Sin limites.')
        return HttpResponseRedirect(reverse('sin_limites'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Acceso del inscrito', 'step': 3, 'total_steps': 3})
        return context
