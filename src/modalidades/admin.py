from django.contrib import admin

from .models import Modalidade


@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']
