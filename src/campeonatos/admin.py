from django.contrib import admin

from .models import Campeonato


@admin.register(Campeonato)
class CampeonatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'modalidade', 'data_inicio', 'data_fim']
    list_filter = ['modalidade']
    search_fields = ['nome']
