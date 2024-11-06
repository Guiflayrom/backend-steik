from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from core.views import (AcrescimoViewSet, BlingOAuthCallbackView,
                        CaixaAbertoView, CaixaViewSet, CategoriaViewSet,
                        DeliveryManagementViewSet, DeliveryViewSet,
                        DespesaViewSet, ExportarTransacoesExcelView,
                        LogoutView, MesaViewSet, MetodoPagamentoViewSet,
                        NotificacaoViewSet, PedidoAtualMesaView, PedidoViewSet,
                        PessoaViewSet, PratoPedidoViewSet, PratoViewSet,
                        RestauranteLoginView, RestauranteViewSet,
                        ResumoVendasView, UsuarioDetalhesView, aaa)

schema_view = get_schema_view(
    openapi.Info(
        title="Steik API",
        default_version="v1",
        description="Documentação da API",
        contact=openapi.Contact(email="guiflayrom@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"restaurantes", RestauranteViewSet)
router.register(
    r"restaurantes/(?P<restaurante_id>\d+)/pratos", PratoViewSet, basename="prato"
)
router.register(
    r"restaurantes/(?P<restaurante_id>\d+)/notificacoes",
    NotificacaoViewSet,
    basename="notificacao",
)
router.register(r"entregas", DeliveryManagementViewSet, basename="entregas")
router.register(r"mesas", MesaViewSet)
router.register(r"prato_pedido", PratoPedidoViewSet)
router.register(r"pedidos", PedidoViewSet)
router.register(r"acrescimos", AcrescimoViewSet)
router.register(r"categorias", CategoriaViewSet)
router.register(r"pessoas", PessoaViewSet)
router.register(r"caixas", CaixaViewSet)
router.register(r"despesas", DespesaViewSet)
router.register(r"metodos_pagamento", MetodoPagamentoViewSet)
router.register(r"deliveries", DeliveryViewSet)

urlpatterns = [
    path("bling/callback/", BlingOAuthCallbackView.as_view(), name="bling_callback"),
    path("bling/", aaa.as_view(), name="bling_callsback"),
    path("api/v1/", include(router.urls)),
    path(
        "api/v1/usuarios/detalhes/",
        UsuarioDetalhesView.as_view(),
        name="usuario-detalhes",
    ),
    path(
        "api/v1/restaurantes/<int:restaurante_id>/mesas/<int:mesa_id>/pedido-atual/",
        PedidoAtualMesaView.as_view(),
        name="pedido_atual_mesa",
    ),
    path(
        "api/v1/restaurantes/caixas/aberto/",
        CaixaAbertoView.as_view(),
        name="caixa-aberto",
    ),
    path("api/v1/login/", RestauranteLoginView.as_view(), name="restaurante_login"),
    path("api/v1/logout/", LogoutView.as_view(), name="logout"),
    path(
        "api/v1/restaurantes/<int:restaurante_id>/caixa/<int:caixa_id>/detalhes/excel/",
        ExportarTransacoesExcelView.as_view(),
        name="exportar-transacoes-excel",
    ),
    path(
        "api/v1/restaurantes/<int:restaurante_id>/caixa/<int:caixa_id>/detalhes/",
        ResumoVendasView.as_view(),
        name="resumo-vendas",
    ),
    path("grappelli/", include("grappelli.urls")),  # Grappelli URL
    path("admin/", admin.site.urls),  # Adiciona o Django Admin às URLs
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
