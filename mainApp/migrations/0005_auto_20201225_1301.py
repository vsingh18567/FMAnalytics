# Generated by Django 3.1.3 on 2020-12-25 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0004_playerseason_value"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playerseason",
            name="tackles",
            field=models.FloatField(),
        ),
    ]
