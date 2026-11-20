from django.urls import path

from . import views

app_name = 'modalidades'

urlpatterns = [
    path('', views.modalidade_list, name='list'),
    path('nova/', views.modalidade_create, name='create'),
    path('<int:pk>/', views.modalidade_detail, name='detail'),
    path('<int:pk>/editar/', views.modalidade_update, name='update'),
    path('<int:pk>/excluir/', views.modalidade_delete, name='delete'),
]
