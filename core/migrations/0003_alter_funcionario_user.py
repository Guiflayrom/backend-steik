# Generated by Django 5.1.1 on 2024-10-25 14:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_pessoa_remove_pedido_cliente_funcionario_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="funcionario",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="funcionario",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
