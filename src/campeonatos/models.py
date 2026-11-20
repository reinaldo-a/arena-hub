from django.core.exceptions import ValidationError
from django.db import models

from modalidades.models import Modalidade


class Campeonato(models.Model):
    nome = models.CharField(max_length=100)
    modalidade = models.ForeignKey(
        Modalidade,
        on_delete=models.PROTECT,
        related_name='campeonatos',
    )
    data_inicio = models.DateField('data de início')
    data_fim = models.DateField('data de término')

    class Meta:
        ordering = ['-data_inicio', 'nome']
        verbose_name = 'campeonato'
        verbose_name_plural = 'campeonatos'

    def __str__(self):
        return self.nome

    def clean(self):
        if self.data_inicio and self.data_fim and self.data_fim < self.data_inicio:
            raise ValidationError({'data_fim': 'A data de término não pode ser anterior à data de início.'})
