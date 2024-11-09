from rest_framework import serializers

from .models import (Acrescimo, Caixa, Categoria, Delivery, Despesa, Mesa,
                     MetodoPagamento, Notificacao, Pedido, Pessoa, Prato,
                     PratoPedido, Restaurante)


class RestauranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurante
        fields = "__all__"


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"


class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = "__all__"


class PratoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.StringRelatedField(source="categoria", read_only=True)
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    restaurante_id = serializers.IntegerField(
        source="restaurante.id", read_only=True
    )  # Novo campo

    class Meta:
        model = Prato
        fields = "__all__"


class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = "__all__"


class NotificacaoSerializer(serializers.ModelSerializer):
    restaurante_id = serializers.IntegerField(
        source="restaurante.id", read_only=True
    )  # Novo campo

    class Meta:
        model = Notificacao
        fields = "__all__"


class PratoPedidoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()  # Accepts ID for creation
    qtd = serializers.IntegerField(source="quantidade")
    prato = PratoSerializer(read_only=True)  # Campo aninhado para todos os dados do prato

    class Meta:
        model = PratoPedido
        fields = [
            "id",
            "qtd",
            "prato",
        ]  # Inclui o campo "prato" com todos os dados do prato

    def create(self, validated_data):
        prato_id = validated_data.pop("id")
        prato = Prato.objects.get(id=prato_id)
        quantidade = validated_data.get("quantidade")
        prato_pedido = PratoPedido.objects.create(prato=prato, quantidade=quantidade)
        return prato_pedido


class CaixaSerializer(serializers.ModelSerializer):
    # operador = serializers.CharField(source='operador.funcionario.nome', read_only=True)

    class Meta:
        model = Caixa
        fields = "__all__"


class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = "__all__"


class MetodoPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPagamento
        fields = "__all__"


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"


class AcrescimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acrescimo
        fields = "__all__"


class PedidoSerializer(serializers.ModelSerializer):
    pessoa = PessoaSerializer(required=False)  # Define pessoa como opcional
    items = PratoPedidoSerializer(many=True, write_only=True)
    total_pratos = serializers.SerializerMethodField()
    horario_pedido = serializers.SerializerMethodField()
    pagamentos = MetodoPagamentoSerializer(
        many=True, required=False, write_only=True
    )  # Pagamentos opcionais
    pagamentos_detail = MetodoPagamentoSerializer(
        many=True, read_only=True, source="pagamentos"
    )  # Read-only field para exibir pagamentos

    restaurante = serializers.PrimaryKeyRelatedField(
        queryset=Restaurante.objects.all(), required=False
    )
    caixa = serializers.PrimaryKeyRelatedField(
        queryset=Caixa.objects.all(), required=False
    )  # Caixa agora é realmente opcional

    class Meta:
        model = Pedido
        fields = [
            "id",
            "pessoa",
            "horario_pedido",
            "status",
            "valor_pago",
            "items",
            "caixa",
            "mesa",
            "desconto",
            "codigo",
            "troco",
            "data_pedido",
            "taxa_entrega",
            "subtotal",
            "is_delivery",
            "observacao",
            "taxa_entrega",
            "total_pratos",
            "pagamentos",
            "pagamentos_detail",  # Campo para exibir detalhes de pagamentos
            "restaurante",  # Novo campo para identificar o restaurante
        ]

    def get_total_pratos(self, obj):
        return sum(
            prato_pedido.prato.valor * prato_pedido.quantidade
            for prato_pedido in obj.pratos.all()
        )

    def get_horario_pedido(self, obj):
        return f"{obj.horario_pedido.hour}:{obj.horario_pedido.minute}"

    def create(self, validated_data):
        pessoa_data = validated_data.pop("pessoa", None)  # Extrai pessoa, se fornecida
        items_data = validated_data.pop("items")
        pagamentos_data = validated_data.pop("pagamentos", [])  # Pagamentos opcionais

        # Caixa e Restaurante como opcionais
        caixa = validated_data.pop("caixa", None)
        restaurante = validated_data.pop("restaurante", None)

        # Verifica se ambos os campos `caixa` e `restaurante` estão ausentes
        if not caixa and not restaurante:
            raise serializers.ValidationError(
                "É necessário fornecer o caixa ou o restaurante para identificar o pedido."
            )

        # Se o restaurante for fornecido mas o caixa não, tenta identificar o caixa aberto do restaurante
        if not caixa and restaurante:
            caixa_aberto = Caixa.objects.filter(
                restaurante=restaurante, fechado_em__isnull=True
            ).first()
            if not caixa_aberto:
                raise serializers.ValidationError(
                    "Nenhum caixa aberto foi encontrado para o restaurante fornecido."
                )
            caixa = caixa_aberto

        # Atualização ou criação da Pessoa, se fornecida
        pessoa = None
        if pessoa_data:
            pessoa, _ = Pessoa.objects.update_or_create(
                cpf_cnpj=pessoa_data.get("cpf_cnpj"), defaults=pessoa_data
            )

        # Criação do Pedido com a pessoa associada, se fornecida
        print(validated_data)
        pedido = Pedido.objects.create(pessoa=pessoa, caixa=caixa, **validated_data)

        # Criação dos PratoPedidos e adição ao Pedido
        prato_pedidos = [
            PratoPedido.objects.create(
                prato=Prato.objects.get(id=item_data["id"]),
                quantidade=item_data["quantidade"],
            )
            for item_data in items_data
        ]
        pedido.pratos.add(*prato_pedidos)

        # Criação dos Métodos de Pagamento e adição ao Pedido
        pagamentos = [
            MetodoPagamento.objects.create(**pagamento_data)
            for pagamento_data in pagamentos_data
        ]
        pedido.pagamento.add(*pagamentos)

        return pedido

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["items"] = PratoPedidoSerializer(
            instance.pratos.all(), many=True
        ).data
        return representation


class SimplePedidoSerializer(serializers.ModelSerializer):
    data_pedido = serializers.DateField(format="%d/%m/%Y")
    horario_pedido = serializers.DateTimeField(format="%H:%M:%S")

    class Meta:
        model = Pedido
        fields = ["codigo", "data_pedido", "horario_pedido", "status"]


class MesaEPedidosSerializer(serializers.ModelSerializer):
    pedidos = SimplePedidoSerializer(many=True, read_only=True, source="pedido_set")

    class Meta:
        model = Mesa
        fields = "__all__"
