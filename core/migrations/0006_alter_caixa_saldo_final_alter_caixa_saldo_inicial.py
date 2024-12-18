# Generated by Django 5.1.1 on 2024-10-25 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_alter_caixa_operador"),
    ]

    operations = [
        migrations.AlterField(
            model_name="caixa",
            name="saldo_final",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="caixa",
            name="saldo_inicial",
            field=models.FloatField(default=0),
        ),
    ]
