# Generated by Django 5.1.1 on 2024-10-25 21:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_alter_caixa_operador"),
    ]

    operations = [
        migrations.AlterField(
            model_name="caixa",
            name="operador",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="caixas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]