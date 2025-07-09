# myapp/urls.py
from django.urls import path, include # Importe 'include'
from rest_framework.routers import DefaultRouter # Importe DefaultRouter
from . import views
from . import views_api # Importe seu novo arquivo de views da API

# Crie um roteador para suas APIs
router = DefaultRouter()
# Adicione o basename explicitamente para ViewSets que usam get_queryset()
router.register(r'republicas', views_api.RepublicaViewSet, basename='republica') # RepublicaViewSet já tem queryset, mas adicionar não faz mal
router.register(r'pessoas', views_api.PessoaViewSet, basename='pessoa')
router.register(r'contas', views_api.ContaViewSet, basename='conta')
router.register(r'pagamentos', views_api.PagamentoViewSet, basename='pagamento')


urlpatterns = [
    path('', views.principal, name='principal'),
    path('pessoas', views.pessoa, name='pessoas'), # Views tradicionais
    path('pagamentos', views.pagamentos, name='pagamentos'), # Views tradicionais
    path('contas', views.contas, name='contas'), # Views tradicionais

    # URLs para contas (tradicionais)
    path('cadastrar_conta', views.cadastrar_conta, name='cadastrar_conta'),

    # URLs para pagamentos (tradicionais)
    path('adicionar_pagamento', views.adicionar_pagamento, name='adicionar_pagamento'),

    # URLs da API REST
    path('api/', include(router.urls)), # Inclua as URLs geradas pelo roteador
]
