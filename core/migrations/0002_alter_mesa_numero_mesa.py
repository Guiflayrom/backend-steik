# Generated by Django 5.1.1 on 2024-09-05 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mesa",
            name="numero_mesa",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]