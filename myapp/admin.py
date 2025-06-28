from .forms import PagamentoForm
from django.contrib import admin
from .models import Republica, Pessoa, Conta, Pagamento

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    form = PagamentoForm

# Register your models here.

admin.site.register(Republica)
admin.site.register(Pessoa)
admin.site.register(Conta)
#admin.site.register(Pagamento)
