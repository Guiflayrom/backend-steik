from django.contrib import admin

from .models import (Caixa, Categoria, Delivery, Despesa, Funcionario, Mesa,
                     MetodoPagamento, Notificacao, Pedido, Pessoa, Prato,
                     PratoPedido, Restaurante, User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "restaurante")
    list_filter = ("restaurante",)


class PratoInline(admin.TabularInline):
    model = Prato
    extra = 1


class MesaInline(admin.TabularInline):
    model = Mesa
    extra = 1


class CategoriaInline(admin.TabularInline):
    model = Categoria
    extra = 1


class FuncionarioInline(admin.TabularInline):
    model = Funcionario
    extra = 1  # Número de linhas extras vazias para adicionar novos funcionários


class RestauranteAdmin(admin.ModelAdmin):
    list_display = ("nome", "localizacao")
    inlines = [PratoInline, MesaInline, CategoriaInline, FuncionarioInline]


class PratoAdmin(admin.ModelAdmin):
    list_display = ("nome", "valor", "restaurante")
    list_filter = ("restaurante",)


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "restaurante")
    list_filter = ("restaurante",)


class MesaAdmin(admin.ModelAdmin):
    list_display = ("numero_mesa", "lugares", "restaurante")
    list_filter = ("restaurante",)


class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "get_nome_pessoa",
        "get_nome_funcionario",
        "status",
        "mesa",
        "codigo",
        "horario_pedido",
        "get_restaurante",
    )
    list_filter = ("caixa__restaurante", "status")

    def get_nome_pessoa(self, obj):
        return obj.pessoa.nome if obj.pessoa else "Sem Pessoa"

    get_nome_pessoa.short_description = "Nome da Pessoa"

    def get_nome_funcionario(self, obj):
        return (
            obj.pessoa.funcionario.user.username
            if obj.pessoa and hasattr(obj.pessoa, "funcionario")
            else "Sem Funcionário"
        )

    get_nome_funcionario.short_description = "Nome do Funcionário"

    def get_restaurante(self, obj):
        return (
            obj.caixa.restaurante.nome
            if obj.caixa and obj.caixa.restaurante
            else "Sem Restaurante"
        )

    get_restaurante.short_description = "Restaurante"


class PratoPedidoAdmin(admin.ModelAdmin):
    list_display = ("prato", "quantidade")


class PessoaAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "email", "restaurante")
    list_filter = ("restaurante",)


class FuncionarioAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "telefone",
        "email",
        "restaurante",
        "pode_acessar_pdv",
        "pode_acessar_garcom",
        "pode_acessar_cozinha",
    )
    list_filter = (
        "restaurante",
        "pode_acessar_pdv",
        "pode_acessar_garcom",
        "pode_acessar_cozinha",
    )

    def nome(self, obj):
        return obj.nome

    def telefone(self, obj):
        return obj.telefone

    def email(self, obj):
        return obj.email


class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ("texto", "visualizada", "restaurante")
    list_filter = ("restaurante",)


class CaixaAdmin(admin.ModelAdmin):
    list_display = ("operador", "saldo_inicial", "aberto_em", "fechado_em", "restaurante")
    list_filter = ("restaurante",)


class DespesaAdmin(admin.ModelAdmin):
    list_display = ("descricao", "valor", "categoria", "caixa")
    list_filter = ("categoria", "caixa")


class MetodoPagamentoAdmin(admin.ModelAdmin):
    list_display = ("metodo", "valor")


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("pedido", "pagamento", "status")
    list_filter = ("status",)


# Registra todos os modelos no admin
admin.site.register(Restaurante, RestauranteAdmin)
admin.site.register(Prato, PratoAdmin)
admin.site.register(Mesa, MesaAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(PratoPedido, PratoPedidoAdmin)
admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Notificacao, NotificacaoAdmin)
admin.site.register(Caixa, CaixaAdmin)
admin.site.register(Despesa, DespesaAdmin)
admin.site.register(MetodoPagamento, MetodoPagamentoAdmin)
admin.site.register(Delivery, DeliveryAdmin)
