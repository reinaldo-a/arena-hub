from django.urls import path

from . import views

app_name = 'campeonatos'

urlpatterns = [
    path('', views.campeonato_list, name='list'),
    path('novo/', views.campeonato_create, name='create'),
    path('<int:pk>/', views.campeonato_detail, name='detail'),
    path('<int:pk>/editar/', views.campeonato_update, name='update'),
    path('<int:pk>/excluir/', views.campeonato_delete, name='delete'),
]
