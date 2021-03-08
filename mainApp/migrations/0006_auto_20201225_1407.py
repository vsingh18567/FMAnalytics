# Generated by Django 3.1.3 on 2020-12-25 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0005_auto_20201225_1301"),
    ]

    operations = [
        migrations.RenameField(
            model_name="player",
            old_name="positions",
            new_name="best_role",
        ),
        migrations.AddField(
            model_name="playerseason",
            name="best_role",
            field=models.CharField(default="na", max_length=4),
            preserve_default=False,
        ),
    ]
