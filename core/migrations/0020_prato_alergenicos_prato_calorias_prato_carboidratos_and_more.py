# Generated by Django 5.1.1 on 2024-10-27 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_alter_pedido_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="prato",
            name="alergenicos",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="prato",
            name="calorias",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="prato",
            name="carboidratos",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="prato",
            name="gorduras",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="prato",
            name="ingredientes",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name="prato",
            name="proteinas",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
