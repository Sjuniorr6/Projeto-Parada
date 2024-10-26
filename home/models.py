from django.db import models
from django.utils import timezone

class Voucher(models.Model):
    Nome_da_empresa = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=50)
    Nome_do_motorista = models.CharField(max_length=50)
    Numero_da_cnh = models.CharField(max_length=50)
    placa_do_carro = models.CharField(max_length=50)
    data = models.DateField()
    qr_code = models.TextField(blank=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=40.00)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.Nome_do_motorista

class Comprovante(models.Model):
    voucher = models.ForeignKey(Voucher, related_name='comprovantes', on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='comprovantes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comprovante de {self.voucher.Nome_do_motorista}"
