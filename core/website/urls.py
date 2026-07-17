from django.urls import path

from core.website.views import (
    HomeView,
    RegistroPaso1View,
    RegistroPaso2View,
    RegistroPaso3View,
    SinLimitesLoginView,
    SinLimitesView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home_public'),
    path('sin-limites/', SinLimitesView.as_view(), name='sin_limites'),
    path('sin-limites/registro/', RegistroPaso1View.as_view(), name='sin_limites_registro'),
    path('sin-limites/registro/padres/', RegistroPaso2View.as_view(), name='sin_limites_registro_padres'),
    path('sin-limites/registro/cuenta/', RegistroPaso3View.as_view(), name='sin_limites_registro_cuenta'),
    path('sin-limites/ingresar/', SinLimitesLoginView.as_view(), name='sin_limites_login'),
]
