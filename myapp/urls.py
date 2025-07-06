from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),
    path('pessoas', views.pessoa, name='pessoas'),
    path('pagamentos', views.pagamentos, name='pagamentos'),
    path('contas', views.contas, name='contas'),

    # URLs para contas
    path('cadastrar_conta', views.cadastrar_conta, name='cadastrar_conta'),

    # URLs para pagamentos
    path('adicionar_pagamento', views.adicionar_pagamento, name='adicionar_pagamento'),
]
