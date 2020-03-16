from django.contrib import admin

# Register your models here.
from .models import Professor, Module, ModuleInstance, Rating


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'module_code')
    ordering = ('module_name',)
    search_fields = ('module_name', 'module_code')


class professor(admin.ModelAdmin):
    filter_horizontal = ('professor',)

admin.site.register(Professor)
admin.site.register(ModuleInstance, professor)
admin.site.register(Rating)

