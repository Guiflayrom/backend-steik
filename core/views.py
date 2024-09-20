from rest_framework import viewsets
from .models import Prato, Mesa, Pedido, PratoPedido, Notificacao
from .serializers import (
    PratoSerializer,
    MesaSerializer,
    PedidoSerializer,
    PratoPedidoSerializer,
    NotificacaoSerializer
)


class NotificacaoViewSet(viewsets.ModelViewSet):
    queryset = Notificacao.objects.all()
    serializer_class = NotificacaoSerializer


class PratoPedidoViewSet(viewsets.ModelViewSet):
    queryset = PratoPedido.objects.all()
    serializer_class = PratoPedidoSerializer


class PratoViewSet(viewsets.ModelViewSet):
    queryset = Prato.objects.all()
    serializer_class = PratoSerializer


class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
