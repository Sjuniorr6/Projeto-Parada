from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView, RegistroMotoristaCreateView, BaseView, AtualizarSaldoView, VoucherDetailView,RegisterView,SideDetailView
from django.urls import path
from .views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('Home', HomeView.as_view(), name='home'),
    path('registrar-motorista/', RegistroMotoristaCreateView.as_view(), name='registro_motorista_form'),
    path('base/', BaseView.as_view(), name='base'),
    path('atualizar-saldo/<int:pk>/', AtualizarSaldoView.as_view(), name='atualizar_saldo'),
    path('voucher/<int:pk>/', VoucherDetailView.as_view(), name='voucher_detail'),
    path('sideDetailView/<int:pk>/', SideDetailView.as_view(), name='sideDetailView'),
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



