from rest_framework import serializers
from .models import Prato, Mesa, Pedido, PratoPedido, Notificacao
import re


def extrair_numeros(string: str) -> int:
    numeros = re.findall(r"\d", string)
    numero_concatenado = "".join(numeros)
    return int(numero_concatenado)


class PratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prato
        fields = "__all__"


class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
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
        # Busca o prato pelo nome informado
        nome_prato = validated_data.pop("nome")
        prato = Prato.objects.get(nome=nome_prato)

        # Cria o objeto PratoPedido
        prato_pedido = PratoPedido.objects.create(prato=prato, **validated_data)

        return prato_pedido


class PedidoSerializer(serializers.ModelSerializer):
    pratos_obj = PratoPedidoSerializer(
        many=True, write_only=True
    )  # Usa PratoPedidoSerializer para entrada
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
            "pratos_obj",  # Campo para receber os pratos do frontend
            "total_pratos",
        ]

    def get_total_pratos(self, obj):
        total = 0
        for prato_pedido in obj.pratos.all():
            total += prato_pedido.prato.valor * prato_pedido.quantidade
        return total

    def get_horario_pedido(self, obj):
        return str(obj.horario_pedido.hour) + ":" + str(obj.horario_pedido.minute)

    def create(self, validated_data):
        # Extrai os dados dos pratos enviados no JSON
        pratos_data = validated_data.pop("pratos_obj")

        # Cria o pedido
        pedido = Pedido.objects.create(**validated_data)

        # Adiciona os pratos ao pedido
        prato_pedidos = []
        for prato_data in pratos_data:
            prato = Prato.objects.get(
                nome=prato_data["nome"]
            )  # Busca o prato pelo nome
            prato_pedido = PratoPedido.objects.create(
                prato=prato, quantidade=prato_data["quantidade"]
            )
            prato_pedidos.append(prato_pedido)

        # Adiciona todos os PratoPedido ao Pedido usando o método add() para o relacionamento ManyToMany
        pedido.pratos.add(*prato_pedidos)

        return pedido

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["pratos"] = PratoPedidoSerializer(
            instance.pratos.all(), many=True
        ).data
        return representation
