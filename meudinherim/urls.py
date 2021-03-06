"""meudinherim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from principal import views
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views
from caixa.api.viewsets import CategoriaViewSet
from banco.api.viewsets import ContaBancoViewSet
from caixa.api.viewsets import LancamentosCaixaViewSet
from banco.api.viewsets import LancamentosBancoViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'api/categorias', CategoriaViewSet, base_name='categorias')
router.register(r'api/agencias', ContaBancoViewSet, base_name='agencias')
router.register(r'api/carteira', LancamentosCaixaViewSet, base_name='carteira')
router.register(r'api/lancamentos_bancario', LancamentosBancoViewSet, base_name='lancamentos')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^principal/', include('principal.urls', namespace='principal')),
    url(r'^caixa/', include('caixa.urls', namespace='caixa')),
    url(r'^banco/', include('banco.urls', namespace='banco')),
    url(r'^contas_a_pagar/', include('contas_a_pagar.urls', namespace='contas_a_pagar')),
    url(r'^contas_a_receber/', include('contas_a_receber.urls', namespace='contas_a_receber')),
    url(r'^metas/', include('metas.urls', namespace='metas')),
    url(r'^relatorios/', include('relatorio.urls', namespace='relatorios')),
    url(r'^config/', include('config.urls', namespace='config')),
    url(r'^mail/', include('mail.urls', namespace='mail')),
    url('', include(router.urls)),
    url(r'^api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/refresh_token/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = views.error_404
handler500 = views.error_500