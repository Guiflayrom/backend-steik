# Generated by Django 5.1.1 on 2024-10-14 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_alter_prato_categoria"),
    ]

    operations = [
        migrations.AddField(
            model_name="prato",
            name="imagem",
            field=models.URLField(blank=True, null=True),
        ),
    ]