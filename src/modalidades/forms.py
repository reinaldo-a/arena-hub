from django import forms

from .models import Modalidade


class ModalidadeForm(forms.ModelForm):
    class Meta:
        model = Modalidade
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
        }
