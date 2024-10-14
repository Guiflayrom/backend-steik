from django.contrib import admin  # Importar o módulo admin do Django
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    PratoViewSet,
    MesaViewSet,
    PedidoViewSet,
    PratoPedidoViewSet,
    CategoriaViewSet,
    NotificacaoViewSet,
    RestauranteLoginView
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Sua API",
        default_version="v1",
        description="Documentação da API",
        terms_of_service="https://www.seusite.com/terms/",
        contact=openapi.Contact(email="contato@seusite.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r"pratos", PratoViewSet)
router.register(r"mesas", MesaViewSet)
router.register(r"notificacao", NotificacaoViewSet)
router.register(r"prato_pedido", PratoPedidoViewSet)
router.register(r"pedidos", PedidoViewSet)
router.register(r"categorias", CategoriaViewSet)

urlpatterns = [
    path('api/login/', RestauranteLoginView.as_view(), name='restaurante_login'),
    path('grappelli/', include('grappelli.urls')),  # Grappelli URL
    path("admin/", admin.site.urls),  # Adiciona o Django Admin às URLs
    path("api/", include(router.urls)),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
