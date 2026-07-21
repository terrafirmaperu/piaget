from django.urls import path

from core.website.views import (
    CuentaLogrosView,
    CuentaOpcionesView,
    CuentaProgresoView,
    DemoMateriaView,
    DemoOpcionesView,
    HomeView,
    RegistroPaso1View,
    RegistroPaso2View,
    RegistroPaso3View,
    SinLimitesLoginView,
    SinLimitesView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home_public'),
    path('demo/', DemoOpcionesView.as_view(), name='demo_opciones'),
    path('demo/<slug:slug>/', DemoMateriaView.as_view(), name='demo_materia'),
    path('cuenta/logros/', CuentaLogrosView.as_view(), name='cuenta_logros'),
    path('cuenta/progreso/', CuentaProgresoView.as_view(), name='cuenta_progreso'),
    path('cuenta/opciones/', CuentaOpcionesView.as_view(), name='cuenta_opciones'),
    path('sin-limites/', SinLimitesView.as_view(), name='sin_limites'),
    path('sin-limites/registro/', RegistroPaso1View.as_view(), name='sin_limites_registro'),
    path('sin-limites/registro/padres/', RegistroPaso2View.as_view(), name='sin_limites_registro_padres'),
    path('sin-limites/registro/cuenta/', RegistroPaso3View.as_view(), name='sin_limites_registro_cuenta'),
    path('sin-limites/ingresar/', SinLimitesLoginView.as_view(), name='sin_limites_login'),
]
