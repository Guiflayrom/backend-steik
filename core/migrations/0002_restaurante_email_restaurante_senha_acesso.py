# Generated by Django 5.1.1 on 2024-10-14 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurante",
            name="email",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="restaurante",
            name="senha_acesso",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
