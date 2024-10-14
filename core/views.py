from rest_framework import viewsets
from .models import Prato, Mesa, Pedido, PratoPedido, Notificacao, Restaurante, Categoria
from .serializers import (
    PratoSerializer,
    MesaSerializer,
    PedidoSerializer,
    PratoPedidoSerializer,
    NotificacaoSerializer,
    RestauranteSerializer,
    CategoriaSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RestauranteLoginView(APIView):
    def post(self, request):
        # Obter email e senha do request
        email = request.data.get('email')
        senha = request.data.get('senha')

        # Verificar se os campos foram fornecidos
        if not email or not senha:
            return Response({"error": "E-mail e senha são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        # Tentar encontrar o restaurante no banco de dados
        try:
            restaurante = Restaurante.objects.get(email=email, senha_acesso=senha)
            # Se encontrar, retornar o ID do restaurante
            return Response({"id": restaurante.id}, status=status.HTTP_200_OK)
        except Restaurante.DoesNotExist:
            # Se não encontrar, retornar erro
            return Response({"error": "E-mail ou senha incorretos."}, status=status.HTTP_401_UNAUTHORIZED)


class RestauranteViewSet(viewsets.ModelViewSet):
    queryset = Restaurante.objects.all()
    serializer_class = RestauranteSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


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
