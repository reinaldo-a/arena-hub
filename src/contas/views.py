from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods, require_POST


@login_required
def home(request):
    return render(request, 'contas/home.html')


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    proxima = request.POST.get('next') or request.GET.get('next', '')
    form = AuthenticationForm(request, data=request.POST or None)
    for campo in form.fields.values():
        campo.widget.attrs['class'] = 'form-control'

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, f'Bem-vindo(a), {form.get_user().username}!')
        if url_has_allowed_host_and_scheme(proxima, allowed_hosts={request.get_host()},
                                           require_https=request.is_secure()):
            return redirect(proxima)
        return redirect('home')

    return render(request, 'contas/login.html', {'form': form, 'next': proxima})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('contas:login')
