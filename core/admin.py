from django.contrib import admin
from .models import Prato, Mesa, Pedido


@admin.register(Prato)
class PratoAdmin(admin.ModelAdmin):
    list_display = ["nome", "numero_prato"]


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ["numero_mesa", "lugares"]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["nome_cliente", "horario_pedido", "status", "mesa"]
    list_filter = ["status", "mesa"]
    search_fields = ["nome_cliente"]
