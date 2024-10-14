from django.contrib import admin
from .models import Restaurante, Notificacao, Prato, Mesa, Pedido, Categoria


class PratoInline(admin.TabularInline):
    model = Prato
    extra = 1  # Número de linhas extras vazias para adicionar novos pratos


class MesaInline(admin.TabularInline):
    model = Mesa
    extra = 1  # Número de linhas extras vazias para adicionar novas mesas


class CategoriaInline(admin.TabularInline):
    model = Categoria
    extra = 1  # Número de linhas extras vazias para adicionar novas mesas

class PedidoInline(admin.TabularInline):
    model = Pedido
    extra = 1  # Número de linhas extras vazias para adicionar novos pedidos


class RestauranteAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "localizacao",
    )  # Exibe o nome e localização na lista de restaurantes
    inlines = [
        PratoInline,
        MesaInline,
        PedidoInline,
    ]  # Exibe pratos, mesas e pedidos inline no admin do restaurante


class PratoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "valor",
        "restaurante",
    )  # Exibe nome do prato, valor e o restaurante ao qual pertence
    list_filter = ("restaurante",)  # Filtra os pratos por restaurante no admin


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "restaurante")
    list_filter = ("restaurante",)


class MesaAdmin(admin.ModelAdmin):
    list_display = ("numero_mesa", "lugares", "restaurante")
    list_filter = ("restaurante",)


class PedidoAdmin(admin.ModelAdmin):
    list_display = ("nome_cliente", "status", "mesa", "horario_pedido", "restaurante")
    list_filter = ("restaurante", "status")


class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ("texto", "visualizada", "restaurante")
    list_filter = ("restaurante",)


# Registra os modelos no admin
admin.site.register(Restaurante, RestauranteAdmin)
admin.site.register(Prato, PratoAdmin)
admin.site.register(Mesa, MesaAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Notificacao, NotificacaoAdmin)
