# Generated by Django 5.1.1 on 2024-11-06 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0021_alter_pedido_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="pedido",
            name="data_pedido",
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
