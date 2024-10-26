from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, TemplateView, DetailView, View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Voucher, Comprovante
from .forms import RegistroMotoristaForm
import qrcode
from io import BytesIO
import base64
from django.http import JsonResponse
from django.utils import timezone
import pytz
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

class HomeView(ListView):
    model = Voucher
    template_name = 'home.html'
    context_object_name = 'vouchers'

    def get_queryset(self):
        now = timezone.now()
        queryset = Voucher.objects.filter(
            saldo__gt=Decimal('0.00'),
            created_at__gte=now - timezone.timedelta(hours=24)
        )
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Nome_da_empresa__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context



class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Nome de usuário já existe')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, 'Usuário criado com sucesso')
                return redirect('login')
        else:
            messages.error(request, 'Senhas não coincidem')
        return render(request, 'register.html')




class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos')
            return render(request, 'login.html')



class BaseView( TemplateView):
    template_name = 'base.html'

class RegistroMotoristaCreateView(  CreateView):
    model = Voucher
    form_class = RegistroMotoristaForm
    template_name = 'registro_motorista_form.html'
    success_url = reverse_lazy('home')
    permission_required = 'app.add_voucher'

    def form_valid(self, form):
        self.object = form.save()
        data = form.cleaned_data
        qr_data = f"Nome: {data['Nome_do_motorista']}\nCNPJ: {data['cnpj']}\nValor: R$ 40.00"
        # Gerar o QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=4,
        )
        qr.add_data(f"http://127.0.0.1:8000/voucher/{self.object.id}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        self.object.qr_code = img_str
        self.object.save()
        return super().form_valid(form)


# Defina o fuso horário para São Paulo, Brasil
BRAZIL_TZ = pytz.timezone('America/Sao_Paulo')

class AtualizarSaldoView( View):
    def post(self, request, pk):
        voucher = get_object_or_404(Voucher, pk=pk)
        valor_utilizado = request.POST.get('valor')
        # Se o valor não for fornecido, use zero
        if not valor_utilizado:
            valor_utilizado = Decimal('0.00')
        else:
            valor_utilizado = Decimal(valor_utilizado)
        # Verificar se o valor a ser subtraído é maior que o saldo atual
        if valor_utilizado > voucher.saldo:
            return render(request, 'voucher_detail.html', {
                'voucher': voucher,
                'error_message': f'O saldo atual é R$ {voucher.saldo}'
            })
        # Atualizar saldo
        voucher.saldo -= valor_utilizado
        # Adicionar comprovantes
        if 'comprovante' in request.FILES:
            for file in request.FILES.getlist('comprovante'):
                Comprovante.objects.create(voucher=voucher, imagem=file)
                voucher.save()
        return HttpResponseRedirect(reverse_lazy('home'))

    def get(self, request, pk):
        return HttpResponseRedirect(reverse_lazy('home'))

    def get(self, request, pk):
        return HttpResponseRedirect(reverse_lazy('home'))

class VoucherDetailView( DetailView):
    model = Voucher
    template_name = 'voucher_detail.html'
    context_object_name = 'voucher'

class SideDetailView( DetailView):
    model = Voucher
    template_name = 'detailside.html'
    context_object_name = 'voucher'
