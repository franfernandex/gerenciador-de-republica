from django.contrib import admin
from .models import Republica, Pessoa, Conta, Pagamento

# Register your models here.

admin.site.register(Republica)
admin.site.register(Pessoa)
admin.site.register(Conta)
admin.site.register(Pagamento)