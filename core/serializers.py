from rest_framework import serializers
from .models import Prato, Mesa, Pedido
import re


def extrair_numeros(string: str) -> int:
    numeros = re.findall(r"\d", string)
    numero_concatenado = "".join(numeros)
    return int(numero_concatenado)


class PratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prato
        fields = '__all__'


class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    pratos_obj = serializers.ListField(
        child=serializers.DictField(), write_only=True
    )  # noqa
    total_pratos = serializers.SerializerMethodField()
    horario_pedido = serializers.SerializerMethodField()

    def get_total_pratos(self, obj):
        total = 0
        for prato in obj.pratos.all():
            total += prato.valor
        return total

    def get_horario_pedido(self, obj):
        
        return str(obj.horario_pedido.hour) + ":" + str(obj.horario_pedido.minute) # noqa

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
            'total_pratos'
        ]

    def create(self, validated_data):
        # Extrai dados de pratos e mesa
        pratos_data = validated_data.pop(
            "pratos_obj",
        )

        pedido = Pedido.objects.create(**validated_data)

        for prato_data in pratos_data:
            prato = Prato.objects.get(
                numero_prato=extrair_numeros(prato_data["nome"])
            )  # noqa
            pedido.pratos.add(prato)

        return pedido

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["pratos"] = PratoSerializer(
            instance.pratos.all(), many=True
        ).data
        return representation
