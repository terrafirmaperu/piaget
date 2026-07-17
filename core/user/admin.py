from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.user.models import Inscrito, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (('Extra', {'fields': ('dni', 'is_change_password', 'token')}),)


class InscritoInline(admin.StackedInline):
    model = Inscrito
    can_delete = False
    extra = 0


@admin.register(Inscrito)
class InscritoAdmin(admin.ModelAdmin):
    list_display = (
        'nombres',
        'apellidos',
        'edad',
        'genero',
        'celular',
        'activo',
        'created_at',
        'user',
    )
    search_fields = (
        'nombres',
        'apellidos',
        'celular',
        'padre_nombres',
        'madre_nombres',
        'user__username',
    )
    list_filter = ('genero', 'activo', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
