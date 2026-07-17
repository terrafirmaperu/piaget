from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config import settings
from core.dashboard.views import DashboardView, InscritosListView
from core.website.views import (
    HomeView,
    RegistroPaso1View,
    RegistroPaso2View,
    RegistroPaso3View,
    SinLimitesLoginView,
    SinLimitesView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sin-limites/', SinLimitesView.as_view(), name='sin_limites'),
    path('sin-limites/registro/', RegistroPaso1View.as_view(), name='sin_limites_registro'),
    path('sin-limites/registro/padres/', RegistroPaso2View.as_view(), name='sin_limites_registro_padres'),
    path('sin-limites/registro/cuenta/', RegistroPaso3View.as_view(), name='sin_limites_registro_cuenta'),
    path('sin-limites/ingresar/', SinLimitesLoginView.as_view(), name='sin_limites_login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/inscritos/', InscritosListView.as_view(), name='inscritos_list'),
    path('admin/', admin.site.urls),
    path('security/', include('core.security.urls')),
    path('login/', include('core.login.urls')),
    path('user/', include('core.user.urls')),
    path('frm/', include('core.frm.urls')),
    path('scm/', include('core.scm.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
