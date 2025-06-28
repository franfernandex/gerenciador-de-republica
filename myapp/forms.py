from django import forms
from .models import Pagamento, Conta

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = '__all__'

    def init(self, args, **kwargs):
        super().__init__(args, **kwargs)

        # Se estamos editando um pagamento existente
        if self.instance and self.instance.pk:
            self.fields['valor_pago'].initial = self.instance.conta.valor
            self.fields['valor_pago'].disabled = True

        # Se estamos criando um novo pagamento (com conta selecionada)
        elif 'conta' in self.data:
            try:
                conta_id = int(self.data.get('conta'))
                conta = Conta.objects.get(pk=conta_id)
                self.fields['valor_pago'].initial = conta.valor
                self.fields['valor_pago'].disabled = True
            except (ValueError, Conta.DoesNotExist):
                pass

    def clean_valor_pago(self):
        conta = self.cleaned_data.get('conta')
        if conta:
            return conta.valor  # Força o valor da conta
        return self.cleaned_data['valor_pago']