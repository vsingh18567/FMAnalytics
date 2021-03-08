# Generated by Django 3.1.3 on 2020-12-26 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0006_auto_20201225_1407"),
    ]

    operations = [
        migrations.RenameField(
            model_name="playerseason",
            old_name="tackles",
            new_name="tackles_per_90",
        ),
        migrations.AddField(
            model_name="player",
            name="dribbles_per_90",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="player",
            name="goals_per_xG",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="player",
            name="int_per_90",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="player",
            name="key_passes_per_90",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="player",
            name="minutes",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="player",
            name="pass_completion",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="player",
            name="shots_per_90",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="player",
            name="tackles_per_90",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="player",
            name="xG",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="player",
            name="appearances",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="player",
            name="assists",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="player",
            name="average_rating",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="player",
            name="best_role",
            field=models.CharField(default="na", max_length=30),
        ),
        migrations.AlterField(
            model_name="player",
            name="goals",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="player",
            name="home_grown_status",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="player",
            name="max_value",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="player",
            name="pom",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="player",
            name="reds",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="player",
            name="seasons",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="player",
            name="yellows",
            field=models.IntegerField(default=0),
        ),
    ]
