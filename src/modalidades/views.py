from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ModalidadeForm
from .models import Modalidade


@login_required
def modalidade_list(request):
    busca = request.GET.get('q', '').strip()
    modalidades = Modalidade.objects.all()
    if busca:
        modalidades = modalidades.filter(nome__icontains=busca)

    page_obj = Paginator(modalidades, 10).get_page(request.GET.get('page'))
    return render(request, 'modalidades/modalidade_list.html', {
        'page_obj': page_obj,
        'busca': busca,
    })


@login_required
def modalidade_detail(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    return render(request, 'modalidades/modalidade_detail.html', {'modalidade': modalidade})


@login_required
@permission_required('modalidades.add_modalidade', raise_exception=True)
@require_http_methods(['GET', 'POST'])
def modalidade_create(request):
    form = ModalidadeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        modalidade = form.save()
        messages.success(request, f'Modalidade "{modalidade}" cadastrada com sucesso.')
        return redirect('modalidades:detail', pk=modalidade.pk)

    return render(request, 'modalidades/modalidade_form.html', {
        'form': form,
        'titulo': 'Nova modalidade',
    })


@login_required
@permission_required('modalidades.change_modalidade', raise_exception=True)
@require_http_methods(['GET', 'POST'])
def modalidade_update(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    form = ModalidadeForm(request.POST or None, instance=modalidade)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Modalidade "{modalidade}" atualizada com sucesso.')
        return redirect('modalidades:detail', pk=modalidade.pk)

    return render(request, 'modalidades/modalidade_form.html', {
        'form': form,
        'modalidade': modalidade,
        'titulo': 'Editar modalidade',
    })


@login_required
@permission_required('modalidades.delete_modalidade', raise_exception=True)
@require_http_methods(['GET', 'POST'])
def modalidade_delete(request, pk):
    modalidade = get_object_or_404(Modalidade, pk=pk)
    if request.method == 'POST':
        nome = str(modalidade)
        modalidade.delete()
        messages.success(request, f'Modalidade "{nome}" excluída com sucesso.')
        return redirect('modalidades:list')

    return render(request, 'modalidades/modalidade_confirm_delete.html', {'modalidade': modalidade})
