from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView

from core.user.models import Inscrito


class ControlRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Solo usuarios de control (staff) entran al dashboard."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.es_control

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return HttpResponseRedirect(reverse('login'))


class DashboardView(ControlRequiredMixin, TemplateView):
    """Panel de control — usuarios que controlan y evalúan."""

    template_name = 'dashboard/panel.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_inscritos'] = Inscrito.objects.filter(activo=True).count()
        context['inscritos_recientes'] = Inscrito.objects.select_related('user').all()[:8]
        return context


class InscritosListView(ControlRequiredMixin, ListView):
    """Listado de inscritos guardados (Sin limites)."""

    model = Inscrito
    template_name = 'dashboard/inscritos_list.html'
    context_object_name = 'inscritos'
    paginate_by = 25

    def get_queryset(self):
        return Inscrito.objects.select_related('user').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inscritos'
        context['total_inscritos'] = self.get_queryset().count()
        return context
