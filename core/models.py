import string
from datetime import timedelta
from random import choices
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def gerar_codigo():
    # Gera três letras maiúsculas
    letras = "".join(choices(string.ascii_uppercase, k=3))
    # Gera três dígitos numéricos
    numeros = "".join(choices(string.digits, k=3))
    # Retorna o código no formato XXX000
    return letras + numeros


class Restaurante(models.Model):
    email = models.CharField(max_length=255, null=True)
    senha_acesso = models.CharField(max_length=255, null=True)
    nome = models.CharField(max_length=255)
    localizacao = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.nome


class User(AbstractUser):
    restaurante = models.OneToOneField(
        Restaurante, on_delete=models.SET_NULL, null=True, blank=True, related_name="user"
    )


class Pessoa(models.Model):
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.PROTECT, related_name="Pessoas"
    )
    nome = models.CharField(max_length=500, null=True, blank=True)
    cpf_cnpj = models.CharField(max_length=30, null=True, blank=True)
    ddd = models.CharField(max_length=4, null=True, blank=True)
    telefone = models.CharField(max_length=500, null=True, blank=True)
    rg = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    cep = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.CharField(max_length=500, null=True, blank=True)
    numero = models.CharField(max_length=20, null=True, blank=True)
    complemento = models.CharField(max_length=500, null=True, blank=True)
    bairro = models.CharField(max_length=500, null=True, blank=True)
    cidade = models.CharField(max_length=500, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    referencia = models.CharField(max_length=500, null=True, blank=True)
    observacoes = models.CharField(max_length=500, null=True, blank=True)


class Funcionario(Pessoa):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="funcionario", null=True, blank=True
    )
    pode_acessar_pdv = models.BooleanField(default=False)
    pode_acessar_garcom = models.BooleanField(default=False)
    pode_acessar_cozinha = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Mesa(models.Model):
    DISPONIVEL = "Disponível"
    RESERVADA = "Reservada"
    OCUPADA = "Ocupada"

    STATUS_CHOICES = [
        (DISPONIVEL, "Disponível"),
        (RESERVADA, "Reservada"),
        (OCUPADA, "Ocupada"),
    ]

    restaurante = models.ForeignKey(
        "Restaurante", on_delete=models.PROTECT, related_name="mesas"
    )
    numero_mesa = models.IntegerField()
    lugares = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DISPONIVEL)

    class Meta:
        unique_together = ("restaurante", "numero_mesa")

    def __str__(self) -> str:
        return f"Mesa {self.numero_mesa} - {self.status}"


class Caixa(models.Model):
    saldo_inicial = models.FloatField(default=0)
    saldo_final = models.FloatField(blank=True, null=True)
    operador = models.ForeignKey(User, on_delete=models.PROTECT, related_name="caixas")
    aberto_em = models.DateTimeField(auto_now_add=True)
    fechado_em = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    restaurante = models.ForeignKey(
        "Restaurante", on_delete=models.PROTECT, related_name="caixas"
    )

    def calcular_saldo_atual(self):
        # Soma todas as despesas e acréscimos para calcular o saldo atual
        total_despesas = sum(despesa.valor for despesa in self.despesas.all())
        total_acrescimos = sum(acrescimo.valor for acrescimo in self.acrescimos.all())
        return self.saldo_inicial + total_acrescimos - total_despesas

    def save(self, *args, **kwargs):
        # Verifica se já existe um caixa aberto para o restaurante
        if not self.fechado_em:
            caixas_abertos = Caixa.objects.filter(
                restaurante=self.restaurante, fechado_em__isnull=True
            ).exclude(id=self.id)
            if caixas_abertos.exists():
                raise ValidationError(
                    "Já existe um caixa aberto para este restaurante. Feche o caixa anterior antes de abrir um novo."
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Caixa {self.id} - Saldo Inicial: {self.saldo_inicial}"


class Despesa(models.Model):
    caixa = models.ForeignKey(Caixa, on_delete=models.PROTECT, related_name="despesas")
    valor = models.FloatField()
    descricao = models.CharField(max_length=255)
    categoria = models.CharField(
        max_length=255,
        choices=(
            ("suprimentos", "suprimentos"),
            ("manutencao", "manutencao"),
            ("outros", "outros"),
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Verifica se o valor da despesa é maior do que o saldo atual do caixa
        saldo_atual = self.caixa.calcular_saldo_atual()
        if self.valor > saldo_atual:
            raise ValidationError(
                "O valor da despesa não pode ser maior do que o saldo disponível em caixa."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Despesa {self.descricao} - Valor: {self.valor}"


class Acrescimo(models.Model):
    caixa = models.ForeignKey(Caixa, on_delete=models.PROTECT, related_name="acrescimos")
    valor = models.FloatField()
    descricao = models.CharField(max_length=255)
    categoria = models.CharField(
        max_length=255,
        choices=(
            ("suprimentos", "suprimentos"),
            ("outros", "outros"),
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Acrescimo {self.descricao} - Valor: {self.valor}"


class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    image = models.URLField()
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.PROTECT, related_name="categorias"
    )

    def __str__(self) -> str:
        return self.nome


class Prato(models.Model):
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.PROTECT, related_name="pratos"
    )
    imagem = models.URLField(blank=True, null=True)
    numero_prato = models.IntegerField()
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="pratos"
    )
    calorias = models.FloatField(null=True, blank=True)
    proteinas = models.FloatField(null=True, blank=True)
    carboidratos = models.FloatField(null=True, blank=True)
    gorduras = models.FloatField(null=True, blank=True)
    alergenicos = models.CharField(max_length=255, blank=True, null=True)
    ingredientes = models.CharField(max_length=500, blank=True, null=True)

    valor = models.FloatField(null=False)
    tipo = models.CharField(
        max_length=100,
        choices=(("quente", "quente"), ("frio", "frio")),
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ("restaurante", "numero_prato")

    def __str__(self) -> str:
        return self.nome


class PratoPedido(models.Model):
    quantidade = models.IntegerField()
    prato = models.ForeignKey(Prato, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.prato.nome} (QTD: {str(self.quantidade)})"


class MetodoPagamento(models.Model):
    valor = models.FloatField()
    metodo = models.CharField(
        max_length=255,
        choices=(
            ("cartao_credito", "cartao_credito"),
            ("cartao_debito", "cartao_debito"),
            ("pix", "pix"),
            ("boleto", "boleto"),
            ("dinheiro", "dinheiro"),
            ("vale_refeicao", "vale_refeicao"),
        ),
    )

    def __str__(self) -> str:
        return self.metodo + " " + str(self.valor)


class AuthenticationToken(models.Model):
    access_token = models.CharField(max_length=255)
    expires_in = models.IntegerField()
    token_type = models.CharField(max_length=50, default="Bearer")
    scope = models.CharField(max_length=255, blank=True)
    refresh_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField(editable=False)  # Calculado automaticamente

    def save(self, *args, **kwargs):
        # Calcula a data de expiração ao salvar, com base em expires_in
        self.expires_at = timezone.now() + timedelta(seconds=self.expires_in)
        super().save(*args, **kwargs)

    @classmethod
    def get_valid_access_token(cls):
        # Verifica se existe algum token válido (não expirado) no banco
        token = (
            cls.objects.filter(expires_at__gt=timezone.now())
            .order_by("-expires_at")
            .first()
        )
        return token.access_token if token else None

    def __str__(self):
        return f"Token {self.access_token} expira em {self.expires_at}"


class Pedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    caixa = models.ForeignKey("Caixa", on_delete=models.PROTECT, related_name="pedidos")
    pessoa = models.ForeignKey("Pessoa", on_delete=models.PROTECT, null=True, blank=True)
    taxa_entrega = models.FloatField(null=True, blank=True)
    pratos = models.ManyToManyField("PratoPedido", related_name="pedidos")
    valor_pago = models.FloatField(default=0, null=True)
    desconto = models.FloatField(null=True, blank=True)
    troco = models.FloatField(null=True, blank=True)
    subtotal = models.FloatField(null=True, blank=True)
    observacao = models.CharField(max_length=255, default="")
    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT, null=True, blank=True)
    is_delivery = models.BooleanField(default=False)
    status = models.CharField(
        max_length=255,
        choices=[
            ("Em Confirmacao", "Em Confirmacao"),
            ("Em Aberto", "Em Aberto"),
            ("Preparando", "Preparando"),
            ("Pedido Pronto", "Pedido Pronto"),
            ("Fechado", "Fechado"),
            ("Em Rota", "Em Rota"),
            ("Entregue", "Entregue"),
            ("Cancelado", "Cancelado"),
        ],
        default="Em Aberto",
    )
    pagamento = models.ManyToManyField(
        "MetodoPagamento",
        related_name="pedidos",
        blank=True,
    )
    horario_pedido = models.DateTimeField(auto_now_add=True)
    data_pedido = models.DateField(auto_now_add=True, blank=True, null=True)
    codigo = models.CharField(max_length=6, null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        # Gera um código único para o pedido se ele ainda não tiver um
        if not self.codigo:
            novo_codigo = gerar_codigo()
            while Pedido.objects.filter(caixa=self.caixa, codigo=novo_codigo).exists():
                novo_codigo = gerar_codigo()
            self.codigo = novo_codigo

        # Lógica para verificar e limitar pedidos com valor_pago vazio por mesa
        if self.mesa is not None:  # Ignora a lógica se a mesa for None
            if self.valor_pago is None:  # Verifica se o valor_pago está vazio
                # Verifica se já existe um pedido sem valor_pago para a mesma mesa
                # pedidos_abertos = Pedido.objects.filter(
                #     mesa=self.mesa, valor_pago__isnull=True
                # ).exclude(id=self.id)

                # if pedidos_abertos.exists():
                # raise ValidationError("Já existe um pedido em aberto para essa mesa.")

                # Define a mesa como Ocupada se o valor_pago estiver vazio
                self.mesa.status = Mesa.OCUPADA
                self.mesa.save()

            else:
                # Define a mesa como Disponível se o valor_pago estiver preenchido
                self.mesa.status = Mesa.DISPONIVEL
                self.mesa.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.codigo} - {self.status}"


class Delivery(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, related_name="delivery")
    pagamento = models.ForeignKey(
        MetodoPagamento, on_delete=models.PROTECT, related_name="delivery"
    )
    status = models.CharField(
        max_length=255,
        choices=(
            ("preparacao", "preparacao"),
            ("em_rota", "em_rota"),
            ("entregue", "entregue"),
        ),
    )


class Notificacao(models.Model):
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.CASCADE, related_name="notificacoes"
    )
    titulo = models.CharField(max_length=255)
    texto = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=(("pronto", "pronto"), ("novo", "novo"), ("aviso", "aviso")),
        blank=True,
        null=True,
    )
    mesa_texto = models.CharField(max_length=50, blank=True, null=True)
    horario = models.TimeField(auto_now_add=True)
    visualizada = models.BooleanField(default=False)
