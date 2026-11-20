from django.contrib import admin
from django.urls import include, path

from contas.views import home

urlpatterns = [
    path('', home, name='home'),
    path('contas/', include('contas.urls')),
    path('modalidades/', include('modalidades.urls')),
    path('admin/', admin.site.urls),
]
