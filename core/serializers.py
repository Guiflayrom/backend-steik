from rest_framework import serializers
from .models import Prato, Mesa, Pedido, PratoPedido, Notificacao, Restaurante, Categoria
import re


def extrair_numeros(string: str) -> int:
    numeros = re.findall(r"\d", string)
    numero_concatenado = "".join(numeros)
    return int(numero_concatenado)


class RestauranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurante
        fields = "__all__"


class PratoSerializer(serializers.ModelSerializer):
    # Para leitura (GET), usamos o nome da categoria
    categoria_nome = serializers.StringRelatedField(source='categoria', read_only=True)
    # Para escrita (POST, PUT, PATCH), aceitamos o ID da categoria
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())

    class Meta:
        model = Prato
        fields = "__all__"


class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = "__all__"


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = "__all__"


class PratoPedidoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(write_only=True)
    prato = PratoSerializer(read_only=True)

    class Meta:
        model = PratoPedido
        fields = ["nome", "quantidade", "prato"]

    def create(self, validated_data):
        nome_prato = validated_data.pop("nome")
        prato = Prato.objects.get(nome=nome_prato)
        prato_pedido = PratoPedido.objects.create(prato=prato, **validated_data)
        return prato_pedido


class PedidoSerializer(serializers.ModelSerializer):
    pratos_obj = PratoPedidoSerializer(many=True, write_only=True)
    total_pratos = serializers.SerializerMethodField()
    horario_pedido = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = [
            "id",
            "nome_cliente",
            "horario_pedido",
            "status",
            "pratos",
            "mesa",
            "pratos_obj",
            'restaurante',
            "total_pratos",
        ]

    def get_total_pratos(self, obj):
        total = 0
        for prato_pedido in obj.pratos.all():
            total += prato_pedido.prato.valor * prato_pedido.quantidade
        return total

    def get_horario_pedido(self, obj):
        return f"{obj.horario_pedido.hour}:{obj.horario_pedido.minute}"

    def create(self, validated_data):
        print(validated_data)
        pratos_data = validated_data.pop("pratos_obj")
        pedido = Pedido.objects.create(**validated_data)
        prato_pedidos = []
        for prato_data in pratos_data:
            prato = Prato.objects.get(nome=prato_data["nome"])
            prato_pedido = PratoPedido.objects.create(
                prato=prato, quantidade=prato_data["quantidade"]
            )
            prato_pedidos.append(prato_pedido)
        pedido.pratos.add(*prato_pedidos)
        return pedido

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["pratos"] = PratoPedidoSerializer(
            instance.pratos.all(), many=True
        ).data
        return representation
