# Generated by Django 5.1.1 on 2024-10-14 16:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_categoria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prato",
            name="categoria",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pratos",
                to="core.categoria",
            ),
        ),
    ]