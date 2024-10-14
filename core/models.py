from django.db import models
from uuid import uuid4


class Restaurante(models.Model):
    email = models.CharField(max_length=255, null=True)
    senha_acesso = models.CharField(max_length=255, null=True)
    nome = models.CharField(max_length=255)
    localizacao = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.nome


class Notificacao(models.Model):
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.CASCADE, related_name="notificacoes"
    )
    texto = models.CharField(max_length=255)
    visualizada = models.BooleanField(default=False)


class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    image = models.URLField()
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.CASCADE, related_name="categorias"
    )

    def __str__(self) -> str:
        return self.nome


class Prato(models.Model):
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.CASCADE, related_name="pratos"
    )
    imagem = models.URLField(blank=True, null=True)
    numero_prato = models.IntegerField()
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='pratos')
    valor = models.IntegerField(null=False)

    class Meta:
        unique_together = ("restaurante", "numero_prato")

    def __str__(self) -> str:
        return self.nome


class PratoPedido(models.Model):
    quantidade = models.IntegerField()
    prato = models.ForeignKey(Prato, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.prato.nome} (QTD: {str(self.quantidade)})'


class Mesa(models.Model):
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.CASCADE, related_name="mesas"
    )
    numero_mesa = models.IntegerField()
    lugares = models.IntegerField()

    class Meta:
        unique_together = ("restaurante", "numero_mesa")

    def __str__(self) -> str:
        return str(self.numero_mesa)


class Pedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    restaurante = models.ForeignKey(
        Restaurante, on_delete=models.CASCADE, related_name="pedidos"
    )
    nome_cliente = models.CharField(max_length=255)
    pratos = models.ManyToManyField(PratoPedido, blank=True, related_name="pedidos")
    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=255,
        choices=[
            ("Em Aberto", "Em Aberto"),
            ("Preparando", "Preparando"),
            ("Pedido Pronto", "Pedido Pronto"),
            ("Fechado", "Fechado"),
        ],
        default="Em Aberto",
    )
    horario_pedido = models.DateTimeField(auto_now_add=True)
