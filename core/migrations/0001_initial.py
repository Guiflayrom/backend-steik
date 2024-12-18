# Generated by Django 5.1.1 on 2024-10-25 14:10

import uuid

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Caixa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("saldo_inicial", models.IntegerField(default=0)),
                ("saldo_final", models.IntegerField(blank=True, null=True)),
                ("operador", models.CharField(max_length=255)),
                ("aberto_em", models.DateTimeField(auto_now_add=True)),
                ("fechado_em", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Categoria",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nome", models.CharField(max_length=255)),
                ("image", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="Cliente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nome_cliente",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("cpf_cnpj", models.CharField(blank=True, max_length=30, null=True)),
                ("ddd", models.CharField(blank=True, max_length=4, null=True)),
                ("telefone", models.CharField(blank=True, max_length=500, null=True)),
                ("rg", models.CharField(blank=True, max_length=30, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("cep", models.CharField(blank=True, max_length=20, null=True)),
                ("endereco", models.CharField(blank=True, max_length=500, null=True)),
                ("numero", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "complemento",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("bairro", models.CharField(blank=True, max_length=500, null=True)),
                ("cidade", models.CharField(blank=True, max_length=500, null=True)),
                ("uf", models.CharField(blank=True, max_length=2, null=True)),
                ("referencia", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "observacoes",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Mesa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("numero_mesa", models.IntegerField()),
                ("lugares", models.IntegerField()),
                ("reservada", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Restaurante",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.CharField(max_length=255, null=True)),
                ("senha_acesso", models.CharField(max_length=255, null=True)),
                ("nome", models.CharField(max_length=255)),
                ("localizacao", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Despesa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("valor", models.IntegerField()),
                ("descricao", models.CharField(max_length=255)),
                (
                    "categoria",
                    models.CharField(
                        choices=[
                            ("suprimentos", "suprimentos"),
                            ("manutencao", "manutencao"),
                            ("outros", "outros"),
                        ],
                        max_length=255,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "caixa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="despesas",
                        to="core.caixa",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Pedido",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("taxa_entrega", models.IntegerField(blank=True, null=True)),
                ("is_delivery", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Em Aberto", "Em Aberto"),
                            ("Preparando", "Preparando"),
                            ("Pedido Pronto", "Pedido Pronto"),
                            ("Fechado", "Fechado"),
                        ],
                        default="Em Aberto",
                        max_length=255,
                    ),
                ),
                ("horario_pedido", models.DateTimeField(auto_now_add=True)),
                (
                    "caixa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="pedidos",
                        to="core.caixa",
                    ),
                ),
                (
                    "cliente",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.cliente",
                    ),
                ),
                (
                    "mesa",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.mesa",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MetodoPagamento",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("valor", models.IntegerField()),
                (
                    "metodo",
                    models.CharField(
                        choices=[
                            ("cartao_credito", "cartao_credito"),
                            ("cartao_debito", "cartao_debito"),
                            ("pix", "pix"),
                            ("boleto", "boleto"),
                            ("dinheiro", "dinheiro"),
                            ("vale_refeicao", "vale_refeicao"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "pedido",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pagamentos",
                        to="core.pedido",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Delivery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("preparacao", "preparacao"),
                            ("em_rota", "em_rota"),
                            ("entregue", "entregue"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "pagamento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="delivery",
                        to="core.metodopagamento",
                    ),
                ),
                (
                    "pedido",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="delivery",
                        to="core.pedido",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Prato",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("imagem", models.URLField(blank=True, null=True)),
                ("numero_prato", models.IntegerField()),
                ("nome", models.CharField(max_length=255)),
                ("descricao", models.TextField()),
                ("valor", models.IntegerField()),
                (
                    "tipo",
                    models.CharField(
                        blank=True,
                        choices=[("quente", "quente"), ("frio", "frio")],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pratos",
                        to="core.categoria",
                    ),
                ),
                (
                    "restaurante",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="pratos",
                        to="core.restaurante",
                    ),
                ),
            ],
            options={
                "unique_together": {("restaurante", "numero_prato")},
            },
        ),
        migrations.CreateModel(
            name="PratoPedido",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantidade", models.IntegerField()),
                (
                    "prato",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.prato"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="pedido",
            name="pratos",
            field=models.ManyToManyField(related_name="pedidos", to="core.pratopedido"),
        ),
        migrations.CreateModel(
            name="Notificacao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titulo", models.CharField(max_length=255)),
                ("texto", models.CharField(max_length=255)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("pronto", "pronto"),
                            ("novo", "novo"),
                            ("aviso", "aviso"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("mesa_texto", models.CharField(blank=True, max_length=50, null=True)),
                ("horario", models.TimeField(auto_now_add=True)),
                ("visualizada", models.BooleanField(default=False)),
                (
                    "restaurante",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notificacoes",
                        to="core.restaurante",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="mesa",
            name="restaurante",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mesas",
                to="core.restaurante",
            ),
        ),
        migrations.AddField(
            model_name="cliente",
            name="restaurante",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="clientes",
                to="core.restaurante",
            ),
        ),
        migrations.AddField(
            model_name="categoria",
            name="restaurante",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="categorias",
                to="core.restaurante",
            ),
        ),
        migrations.AddField(
            model_name="caixa",
            name="restaurante",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="caixas",
                to="core.restaurante",
            ),
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
                (
                    "restaurante",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="user",
                        to="core.restaurante",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="mesa",
            unique_together={("restaurante", "numero_mesa")},
        ),
    ]
