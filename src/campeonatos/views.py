from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from modalidades.models import Modalidade

from .forms import CampeonatoForm
from .models import Campeonato


@login_required
def campeonato_list(request):
    busca = request.GET.get('q', '').strip()
    modalidade_id = request.GET.get('modalidade', '')

    campeonatos = Campeonato.objects.select_related('modalidade')
    if busca:
        campeonatos = campeonatos.filter(nome__icontains=busca)
    if modalidade_id.isdigit():
        campeonatos = campeonatos.filter(modalidade_id=modalidade_id)

    page_obj = Paginator(campeonatos, 10).get_page(request.GET.get('page'))
    return render(request, 'campeonatos/campeonato_list.html', {
        'page_obj': page_obj,
        'busca': busca,
        'modalidade_id': modalidade_id,
        'modalidades': Modalidade.objects.all(),
    })


@login_required
def campeonato_detail(request, pk):
    campeonato = get_object_or_404(Campeonato.objects.select_related('modalidade'), pk=pk)
    return render(request, 'campeonatos/campeonato_detail.html', {'campeonato': campeonato})


@login_required
@permission_required('campeonatos.add_campeonato', raise_exception=True)
@require_http_methods(['GET', 'POST'])
def campeonato_create(request):
    form = CampeonatoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        campeonato = form.save()
        messages.success(request, f'Campeonato "{campeonato}" cadastrado com sucesso.')
        return redirect('campeonatos:detail', pk=campeonato.pk)

    return render(request, 'campeonatos/campeonato_form.html', {
        'form': form,
        'titulo': 'Novo campeonato',
    })


@login_required
@permission_required('campeonatos.change_campeonato', raise_exception=True)
@require_http_methods(['GET', 'POST'])
def campeonato_update(request, pk):
    campeonato = get_object_or_404(Campeonato, pk=pk)
    form = CampeonatoForm(request.POST or None, instance=campeonato)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Campeonato "{campeonato}" atualizado com sucesso.')
        return redirect('campeonatos:detail', pk=campeonato.pk)

    return render(request, 'campeonatos/campeonato_form.html', {
        'form': form,
        'campeonato': campeonato,
        'titulo': 'Editar campeonato',
    })


@login_required
@permission_required('campeonatos.delete_campeonato', raise_exception=True)
@require_http_methods(['GET', 'POST'])
def campeonato_delete(request, pk):
    campeonato = get_object_or_404(Campeonato, pk=pk)
    if request.method == 'POST':
        nome = str(campeonato)
        campeonato.delete()
        messages.success(request, f'Campeonato "{nome}" excluído com sucesso.')
        return redirect('campeonatos:list')

    return render(request, 'campeonatos/campeonato_confirm_delete.html', {'campeonato': campeonato})
