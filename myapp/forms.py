from django import forms
from .models import Pagamento, Conta, Pessoa
from django.utils import timezone


class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome_conta' , 'valor' , 'data_vencimento']
        widgets = {
            'nome_conta': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Conta de Luz'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'data_vencimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }


class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['conta']
        widgets = {
            'conta': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        self.pessoa = kwargs.pop('pessoa', None)
        super().__init__(*args, **kwargs)

        # Filtrar apenas contas não pagas
        if self.pessoa:
            self.fields['conta'].queryset = Conta.objects.filter(paga=False)
        
    def save(self, commit=True):
        pagamento = super().save(commit=False)

        # Definir automaticamente o valor como o valor total da conta
        pagamento.valor_pago = pagamento.conta.valor

        if commit:
            pagamento.save()
        
        return pagamento
