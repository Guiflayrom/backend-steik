# Generated by Django 5.1.1 on 2024-11-09 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0025_alter_acrescimo_valor_alter_despesa_valor_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pedido",
            name="valor_pago",
            field=models.FloatField(default=0),
        ),
    ]
