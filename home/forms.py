from django import forms
from .models import Voucher, Comprovante

class RegistroMotoristaForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ['Nome_da_empresa', 'cnpj', 'Nome_do_motorista', 'Numero_da_cnh', 'placa_do_carro', 'data']
        widgets = {
            'Nome_da_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'Nome_do_motorista': forms.TextInput(attrs={'class': 'form-control'}),
            'Numero_da_cnh': forms.TextInput(attrs={'class': 'form-control'}),
            'placa_do_carro': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'Nome_da_empresa': 'Nome da Empresa',
            'cnpj': 'CNPJ',
            'Nome_do_motorista': 'Nome do Motorista',
            'Numero_da_cnh': 'Número da CNH',
            'placa_do_carro': 'Placa do Carro',
            'data': 'Data',
        }

class ComprovanteForm(forms.ModelForm):
    class Meta:
        model = Comprovante
        fields = ['imagem']
        widgets = {
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'imagem': 'Comprovante',
        }
