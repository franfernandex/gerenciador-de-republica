from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),
    path('pessoas', views.pessoa, name='pessoas'),  #linha adicionada
    path('pagamentos', views.pagamentos, name='pagamentos'),  #linha adicionada
    path('contas', views.contas, name='contas'),  #linha adicionada

]