# Generated by Django 5.1.1 on 2024-11-08 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0024_pedido_observacao"),
    ]

    operations = [
        migrations.AlterField(
            model_name="acrescimo",
            name="valor",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="despesa",
            name="valor",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="metodopagamento",
            name="valor",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="taxa_entrega",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="prato",
            name="valor",
            field=models.FloatField(),
        ),
    ]
