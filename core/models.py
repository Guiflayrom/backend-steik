from django.db import models
from uuid import uuid4


class Prato(models.Model):
    numero_prato = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    valor = models.IntegerField(null=False)


class Mesa(models.Model):
    numero_mesa = models.IntegerField(primary_key=True)
    lugares = models.IntegerField()

    def __str__(self) -> str:
        return str(self.numero_mesa)


class Pedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome_cliente = models.CharField(max_length=255)
    pratos = models.ManyToManyField(Prato, blank=True, related_name="pedidos")
    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=255,
        choices=[("Em Aberto", "Em Aberto"), ("Fechado", "Fechado")],
        default="Em Aberto",
    )
    horario_pedido = models.DateTimeField(auto_now_add=True)
