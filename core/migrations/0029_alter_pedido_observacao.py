# Generated by Django 5.1.1 on 2024-11-12 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0028_prato_mostrar_cardapio_alter_prato_categoria_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pedido",
            name="observacao",
            field=models.CharField(blank=True, default="", max_length=255, null=True),
        ),
    ]
